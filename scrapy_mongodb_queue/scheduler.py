# -*- coding: utf-8 -*-
# (c) Lhassan Baazzi <baazzilhassan@gmail.com>

import datetime
from scrapy.utils.reqser import request_to_dict, request_from_dict
from . import connection
from .dupefilter import RFPDupeFilter

class Scheduler(object):
    def __init__(self, server, mongodb_db, persist, queue_key, queue_order, debug):
        self.server              = server
        self.mongodb_db          = mongodb_db
        self.queue_key           = queue_key
        self.persist             = persist
        self.queue_order         = queue_order
        self.scheduler_queue_key = '%s_qs' % (queue_key,)
        self.dupfilter_queue_key = '%s_qf' % (queue_key,)
        self.debug               = debug

    def __len__(self):
        return self.client.size()

    @classmethod
    def from_settings(cls, settings):
        mongodb_db     = settings.get('MONGODB_DB', 'scrapy')
        persist        = settings.get('MONGODB_QUEUE_PERSIST', True)
        queue_key      = settings.get('MONGODB_QUEUE_NAME', None)
        queue_type     = settings.get('MONGODB_QUEUE_TYPE', 'FIFO')
        debug          = settings.getbool('DUPEFILTER_DEBUG')

        if queue_type not in ('FIFO', 'LIFO'):
            raise Error('MONGODB_QUEUE_TYPE must be FIFO (default) or LIFO')

        if queue_type == 'LIFO':
            queue_order = -1
        else:
            queue_order = 1

        server = connection.from_settings(settings)

        return cls(server, mongodb_db, persist, queue_key, queue_order, debug)

    @classmethod
    def from_crawler(cls, crawler):
        instance = cls.from_settings(crawler.settings)
        # FIXME: for now, stats are only supported from this constructor
        instance.stats = crawler.stats
        return instance

    def open(self, spider):
        self.spider = spider
        self.db = self.server[self.mongodb_db]
        self.collection = self.db[self.scheduler_queue_key]

        self.df = RFPDupeFilter(self.server, self.mongodb_db, self.dupfilter_queue_key, self.debug)

        # notice if there are requests already in the queue
        size = self.collection.count()
        if size > 0:
            spider.log("Resuming crawl (%d requests scheduled)" % size)

    def close(self, reason):
        if not self.persist:
            self.collection.drop()

    def enqueue_request(self, request):
        if not request.dont_filter and self.df.request_seen(request):
            self.df.log(request, self.spider)
            return

        if self.stats:
            self.stats.inc_value('scheduler/enqueued/mongodb', spider=self.spider)

        self.collection.insert({
            'data': request_to_dict(request, self.spider),
            'created': datetime.datetime.utcnow()
        })

    def next_request(self):
        entry = self.collection.find_and_modify(sort={"$natural": self.queue_order}, remove=True)
        if entry:
            request = request_from_dict(entry['data'], self.spider)
            if request and self.stats:
                self.stats.inc_value('scheduler/dequeued/mongodb', spider=self.spider)

            return request

        return None

    def has_pending_requests(self):
        return self.collection.count() > 0
