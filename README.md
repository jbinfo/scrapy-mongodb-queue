# Scrapy MongoDB Queue
MongoDB-based components for scrapy that allows distributed crawling

Available Scrapy components
---------------------------

* Scheduler
* Duplication Filter

Installation
------------

From `pypi`
```shell
  $ pip install git+https://github.com/jbinfo/scrapy-mongodb-queue
```

From `github`
```shell
  $ git clone https://github.com/jbinfo/scrapy-mongodb-queue.git
  $ cd scrapy-mongodb-queue
  $ python setup.py install
```

Usage
-----

Enable the components in your `settings.py`:

```python
  # Enables scheduling storing requests queue in redis.
  SCHEDULER = "scrapy_mongodb_queue.scheduler.Scheduler"

  # Don't cleanup mongodb queues, allows to pause/resume crawls.
  MONGODB_QUEUE_PERSIST = True

  # Specify the host and port to use when connecting to Redis (optional).
  MONGODB_SERVER = 'localhost'
  MONGODB_PORT = 27017
  MONGODB_DB = "my_db"

  # MongoDB collection name
  MONGODB_QUEUE_NAME = "my_queue"
```

Author
------

This project is maintained by Lhassan Baazzi ([GitHub](https://github.com/jbinfo) | [Twitter](https://twitter.com/baazzilhassan) | [LinkedIn](https://ma.linkedin.com/pub/lhassan-baazzi/49/606/a70))


[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/jbinfo/scrapy-mongodb-queue/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

