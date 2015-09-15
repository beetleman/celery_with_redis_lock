from celery_with_redis_lock.app import add_to_list as _add_to_list
from celery_with_redis_lock.app import get_locked_function
from celery_with_redis_lock.celery import app


@app.task(ignore_result=True)
def add_to_list(x):
    with get_locked_function(_add_to_list, False, x) as func:
        func()
