import time
from itertools import repeat
from multiprocessing import Pool

from celery_with_redis_lock.app import get_list
from celery_with_redis_lock.tasks import add_to_list, TIMEOUT


def run_add_to_list(x):
    add_to_list.delay(x)


def run_in_pool(func, data, sleep=5):
    with Pool(3) as p:
        p.map(func, data)
    time.sleep(sleep)


def test_add_to_list_single_lock(drop_list):
    test_data = list(repeat(1, 10))
    run_in_pool(run_add_to_list, test_data)
    assert [1] == sorted(map(int, get_list()))


def test_add_to_list_many_locks(drop_list):
    test_data = list(repeat(2, 10)) + list(repeat(3, 10)) + list(repeat(4, 10))
    run_in_pool(run_add_to_list, test_data)
    assert [2, 3, 4] == sorted(map(int, get_list()))


def test_add_to_list_many_locks_timeout(drop_list):
    time.sleep(2*TIMEOUT)  # czekam az zejda locki z innych testow
    test_data = list(repeat(5, 10)) + list(repeat(6, 10)) + list(repeat(7, 10))
    run_in_pool(run_add_to_list, test_data, sleep=2*TIMEOUT)
    run_in_pool(run_add_to_list, test_data)
    assert [5, 5, 6, 6, 7, 7] == sorted(map(int, get_list()))
