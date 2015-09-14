import redis
import time
import logging
from hashlib import md5
from contextlib import contextmanager
from functools import partial

LIST_NAME = 'turbo_lista'
TIMEOUT = 30

REDIS_CLIENT = redis.StrictRedis()


def get_storage():
    return REDIS_CLIENT


def add_to_list(x):
    r = get_storage()
    v = r.rpush(LIST_NAME, x)
    time.sleep(4)  # sypuluje jakis dlugi task
    return v


def get_list():
    r = get_storage()
    return r.lrange(LIST_NAME, 0, -1)


@contextmanager
def get_locked_function(func, release, *args):
    args_hash = md5()
    args_hash.update(b'.'.join(
        map(lambda x: str(x).encode(), args)
    ))
    lock_key = args_hash.hexdigest()
    lock = REDIS_CLIENT.lock(lock_key, timeout=TIMEOUT)
    try:
        have_lock = lock.acquire(blocking=False)
        if have_lock:
            logging.info("lock for %s" % lock_key)
            logging.info("run: %s(*%s)" % (func.__name__, args))
            yield partial(func, *args)
        else:
            logging.info("skip: %s(*%s)" % (func.__name__, args))
            yield lambda: 'skiped'
    finally:
        if have_lock and release:
            logging.info("release %s" % lock_key)
            lock.release()
