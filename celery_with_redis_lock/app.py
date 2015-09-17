import time

import redis

LIST_NAME = 'turbo_lista'

REDIS_CLIENT = redis.StrictRedis(db='10')


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
