from __future__ import absolute_import

from celery_with_redis_lock.lock import lock_decorator
from celery import Task

from celery import Task


class _lock_decorator(lock_decorator):

    def get_prefix(self, func, args):
        return self.task_name


class TaskWithLock(Task):
    abstract = True

    lock_release = True
    lock_timeout = None
    lock_redis_client = None
    lock_kwargs = {}

    def __init__(self, *args, **kwargs):
        decorator = self.get_lock_decorator(
            release=self.lock_release,
            timeout=self.lock_timeout,
            redis_client=self.lock_redis_client,
            **self.lock_kwargs
        )
        self.run = decorator(self.run)
        super(TaskWithLock, self).__init__(*args, **kwargs)

    def get_lock_decorator(self, release=True, timeout=None, redis_client=None,
                           **lock_kwargs):
        decorator = _lock_decorator(
            release=release, timeout=timeout, redis_client=redis_client,
            **lock_kwargs
        )
        decorator.task_name = self.name
        return decorator
