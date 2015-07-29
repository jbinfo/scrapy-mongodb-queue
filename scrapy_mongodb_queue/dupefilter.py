# -*- coding: utf-8 -*-
# (c) Lhassan Baazzi <baazzilhassan@gmail.com>

import time
from scrapy.dupefilter import RFPDupeFilter as BaseDupeFilter
from scrapy.utils.request import request_fingerprint
from . import connection

class RFPDupeFilter(BaseDupeFilter):
    """Redis-based request duplication filter"""

    def __init__(self, server, mongodb_db, dupfilter_queue_key, debug):
        self.server = server
        self.dupfilter_queue_key = dupfilter_queue_key

        self.db = server[mongodb_db]
        self.collection = self.db[self.dupfilter_queue_key]

        self.debug = debug
        self.logdupes = True

    @classmethod
    def from_settings(cls, settings):
        mongodb_db     = settings.get('MONGODB_DB', 'scrapy')
        persist        = settings.get('MONGODB_QUEUE_PERSIST', True)
        queue_key      = settings.get('MONGODB_QUEUE_NAME', None)
        debug          = settings.getbool('DUPEFILTER_DEBUG')

        key = "dupefilter:%s" % int(time.time())

        server = connection.from_settings(settings)
        self.db = server[self.mongodb_db]

        return cls(server, mongodb_db, key, debug)

    @classmethod
    def from_crawler(cls, crawler):
        return cls.from_settings(crawler.settings)

    def request_seen(self, request):
        added = True

        fp = request_fingerprint(request)
        result = self.collection.find({'fp': fp}).limit(1)
        if not result.count():
            self.collection.insert({'fp': fp})
            added = False

        return added

    def close(self, reason):
        self.clear()

    def clear(self):
        """Clears fingerprints data"""
        self.collection.drop()
