# -*- coding: utf-8 -*-
# (c) Lhassan Baazzi <baazzilhassan@gmail.com>

from pymongo import MongoClient

# Default values.
MONGODB_SERVER = 'localhost'
MONGODB_PORT   = 27017

def from_settings(settings):
    host = settings.get('MONGODB_SERVER', MONGODB_SERVER)
    port = settings.get('MONGODB_PORT', MONGODB_PORT)

    return MongoClient('mongodb://%s:%d/' % (host, port))
