import logging
from functools import wraps
from hashlib import md5

import redis

DEFAULT_TIMEOUT = 30


class lock_decorator(object):

    def __init__(self, release=True, timeout=None, redis_client=None):
        if timeout is None:
            timeout = DEFAULT_TIMEOUT
        self.timeout = timeout
        self.release = release

    def _create_redis_client(self):
        return redis.StrictRedis()

    @property
    def redis_client(self):
        if hasattr(self, '_redis_client'):
            return self._redis_client
        self._redis_client = self._create_redis_client()
        return self._redis_client

    @redis_client.setter
    def redis_client(self, value):
        self._redis_client = value

    @redis_client.deleter
    def redis_client(self):
        del self._redis_client

    def _create_lock_name(self, args):
        args_hash = md5()
        args_hash.update(b'.'.join(
            map(lambda x: str(x).encode(), args)
        ))
        return args_hash.hexdigest()

    def __call__(self, func):
        decorator = self

        @wraps(func)
        def wrapper(*args):
            lock_key = decorator._create_lock_name(args)
            lock = decorator.redis_client.lock(
                lock_key,
                timeout=decorator.timeout
            )
            try:
                have_lock = lock.acquire(blocking=False)
                if have_lock:
                    logging.info("lock for %s" % lock_key)
                    logging.info("run: %s(*%s)" % (func.__name__, args))
                    func(*args)
                else:
                    logging.info("skip: %s(*%s)" % (func.__name__, args))
            finally:
                if have_lock and decorator.release:
                    logging.info("release %s" % lock_key)
                    lock.release()
        return wrapper
