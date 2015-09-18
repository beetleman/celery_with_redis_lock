import time

import redis

LIST_NAME = 'turbo_lista'

REDIS_CLIENT = redis.StrictRedis(db='10')


def get_storage():
    return REDIS_CLIENT


def add_to_list(x, list_name=LIST_NAME):
    r = get_storage()
    v = r.rpush(list_name, x)
    time.sleep(4)  # sypuluje jakis dlugi task
    return v


def get_list(list_name=LIST_NAME):
    r = get_storage()
    return r.lrange(list_name, 0, -1)
