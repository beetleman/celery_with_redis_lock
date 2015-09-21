import logging
from functools import wraps
from hashlib import md5

import redis

DEFAULT_TIMEOUT = 30


class lock_decorator(object):

    def __init__(self, release=True, timeout=None, redis_client=None,
                 **lock_kwargs):
        if timeout is None:
            timeout = DEFAULT_TIMEOUT
        self.timeout = timeout
        self._redis_client = redis_client
        self.lock_kwargs = lock_kwargs
        self.release = release

    def get_redis_client(self):
        return redis.StrictRedis()

    @property
    def redis_client(self):
        redis_client = getattr(self, '_redis_client', None)
        if redis_client is None:
            self._redis_client = self.get_redis_client()
        return self._redis_client

    @redis_client.setter
    def redis_client(self, value):
        self._redis_client = value

    @redis_client.deleter
    def redis_client(self):
        del self._redis_client

    def get_args_hash(self, func, args):
        args_hash = md5()
        args_hash.update(b'.'.join(
            map(lambda x: str(x).encode(), args)
        ))
        return args_hash.hexdigest()

    def get_prefix(self, func, args):
        return func.__name__

    def get_lock(self, lock_key):
        return self.redis_client.lock(
            lock_key,
            timeout=self.timeout,
            **self.lock_kwargs
        )

    def _get_lock_name(self, args, func):
        prefix = self.get_prefix(args, func)
        args_hash = self.get_args_hash(args, func)
        if prefix is None:
            return args_hash
        else:
            return '%s.%s' % (prefix, args_hash)

    def __call__(self, func):
        decorator = self

        @wraps(func)
        def wrapper(*args):
            lock_key = decorator._get_lock_name(func, args)
            lock = decorator.get_lock(lock_key)
            try:
                have_lock = lock.acquire(blocking=False)
                if have_lock:
                    logging.debug("lock for %s" % lock_key)
                    logging.debug("lock for %s" % lock_key)
                    logging.debug("run: %s(*%s)" % (func.__name__, args))
                    func(*args)
                else:
                    logging.debug("skip: %s(*%s)" % (func.__name__, args))
            finally:
                if have_lock and decorator.release:
                    logging.debug("release %s" % lock_key)
                    lock.release()
        return wrapper


class binded_lock_decorator(lock_decorator):

    def get_prefix(self, func, args):
        return args[0].name

    def get_args_hash(self, func, args):
        return super(binded_lock_decorator, self).get_args_hash(func, args[1:])
