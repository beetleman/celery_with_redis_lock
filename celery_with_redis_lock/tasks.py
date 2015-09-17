from celery_with_redis_lock.app import add_to_list as _add_to_list
from celery_with_redis_lock.app import get_storage
from celery_with_redis_lock.lock import lock_decorator, binded_lock_decorator
from celery_with_redis_lock.celery import app

TIMEOUT = 10


@app.task(ignore_result=True)
@lock_decorator(release=False, timeout=TIMEOUT, redis_client=get_storage())
def add_to_list(x):
    return _add_to_list(x)


@app.task(ignore_result=True, bind=True)
@binded_lock_decorator(release=False, timeout=TIMEOUT, redis_client=get_storage())
def binded_add_to_list(self, x):
    return _add_to_list(x)
