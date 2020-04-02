import os


class ProductionConfig(object):
    CACHE_TYPE = 'memcached'
    CACHE_MEMCACHED_SERVERS = ['127.0.0.1']
    DATABASE_PATH = 'app.db'
    SECRET_KEY = os.environ['CORONASTATS_SECRET_KEY']


class DevelopmentConfig(object):
    CACHE_TYPE = "null"
    DATABASE_PATH = '../app.db'
    DEBUG = True
