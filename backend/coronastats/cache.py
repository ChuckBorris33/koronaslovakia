import os

from flask_caching import Cache

cache_type = os.getenv("CACHE_TYPE", "null")
cache = Cache(config={'CACHE_TYPE': cache_type, 'CACHE_MEMCACHED_SERVERS': ['127.0.0.1']})


def clear_cache():
    cache.clear()
