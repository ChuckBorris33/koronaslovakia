import os


class ProductionConfig(object):
    CACHE_TYPE = "memcached"
    CACHE_MEMCACHED_SERVERS = ["127.0.0.1"]
    DATABASE = "sqlite:///app.db"
    SECRET_KEY = os.environ["CORONASTATS_SECRET_KEY"]


class DevelopmentConfig(object):
    CACHE_TYPE = "null"
    DATABASE = "sqlite:///../app.db"
    DEBUG = True


class TestConfig(object):
    CACHE_TYPE = "simple"
    DATABASE_PATH = "tests/testing.db"
    DATABASE = f"sqlite:///{DATABASE_PATH}"
    TEST = True
