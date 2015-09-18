from celery_with_redis_lock.lock import lock_decorator, binded_lock_decorator

from .app import add_to_list as _add_to_list
from .app import get_storage
from .celery import app

TIMEOUT = 20


@app.task()
@lock_decorator(release=False, timeout=TIMEOUT, redis_client=get_storage())
def add_to_list(x, list_name):
    return _add_to_list(x, list_name)


@app.task(bind=True)
@binded_lock_decorator(release=False, timeout=TIMEOUT, redis_client=get_storage())
def binded_add_to_list(self, x, list_name):
    return _add_to_list(x, list_name)
