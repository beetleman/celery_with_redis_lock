import time
from itertools import repeat
from multiprocessing import Pool

import pytest

from celery_with_redis_lock.app import get_list
from celery_with_redis_lock.tasks import (
    add_to_list,
    binded_add_to_list,
    TIMEOUT
)


def run_add_to_list(x):
    add_to_list.delay(x)


def run_binded_add_to_list(x):
    binded_add_to_list.delay(x)


test_data = (
    (list(repeat(1, 10)), [1]),
    (list(repeat(2, 10)) + list(repeat(3, 10)) +
     list(repeat(4, 10)), [2, 3, 4]),
)
test_function = (
    run_add_to_list,
    run_binded_add_to_list,
)


def run_in_pool(func, data, sleep=10):
    with Pool(3) as p:
        p.map(func, data)
    time.sleep(sleep)


@pytest.mark.parametrize("function", test_function)
@pytest.mark.parametrize("tested,expected", test_data)
def test_add_to_list(drop_db, tested, expected, function):
    run_in_pool(function, tested)
    assert expected == sorted(map(int, get_list()))


@pytest.mark.parametrize("function", test_function)
def test_add_to_list_many_locks_timeout(drop_db, function):
    test_data = list(repeat(5, 10)) + list(repeat(6, 10)) + list(repeat(7, 10))
    run_in_pool(function, test_data, sleep=2 * TIMEOUT)
    run_in_pool(function, test_data)
    assert [5, 5, 6, 6, 7, 7] == sorted(map(int, get_list()))
