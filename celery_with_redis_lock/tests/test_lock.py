import time
from itertools import repeat
from multiprocessing import Pool

from celery_with_redis_lock.app import get_list
from celery_with_redis_lock.tasks import add_to_list


def run_add_to_list(x):
    add_to_list.delay(x)


def test_add_to_list(drop_list):
    test_data = list(repeat(1, 10))
    with Pool(3) as p:
        p.map(run_add_to_list, test_data)
    time.sleep(5)
    assert [1] == sorted(map(int, get_list()))
