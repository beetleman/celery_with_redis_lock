from celery_many_producers.celery import app
from celery_many_producers.app import add_to_list as _add_to_list
from celery_many_producers.app import get_locked_function


@app.task(ignore_result=True)
def add_to_list(x):
    with get_locked_function(_add_to_list, False, x) as func:
        func()
