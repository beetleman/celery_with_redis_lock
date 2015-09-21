from celery_with_redis_lock.lock import lock_decorator, binded_lock_decorator
from celery_with_redis_lock.tasks import TaskWithLock


from .app import add_to_list as _add_to_list
from .app import get_storage
from .celery import app

TIMEOUT = 20


class BaseTask(TaskWithLock):
    lock_release = False
    lock_timeout = TIMEOUT
    lock_redis_client = get_storage()


@app.task()
@lock_decorator(release=False, timeout=TIMEOUT, redis_client=get_storage())
def add_to_list(x, list_name):
    return _add_to_list(x, list_name)


@app.task(bind=True)
@binded_lock_decorator(release=False, timeout=TIMEOUT, redis_client=get_storage())
def binded_add_to_list(self, x, list_name):
    return _add_to_list(x, list_name)


@app.task(base=BaseTask)
def add_to_list_base_class(x, list_name):
    return _add_to_list(x, list_name)
