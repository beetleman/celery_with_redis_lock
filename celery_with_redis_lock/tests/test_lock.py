from __future__ import absolute_import

import time
from itertools import repeat
from multiprocessing import Pool

import pytest

from example_app.app import get_list
from example_app.tasks import (
    add_to_list,
    binded_add_to_list,
    add_to_list_base_class,
    TIMEOUT
)


def run_add_to_list(args):
    r = add_to_list.delay(*args)
    r.wait()


def run_binded_add_to_list(args):
    r = binded_add_to_list.delay(*args)
    r.wait()


def run_add_to_list_base_class(args):
    r = add_to_list_base_class.delay(*args)
    r.wait()


def run_in_pool(func, data, sleep=0):
    p = Pool(len(data))  # race condition simulation
    p.map(func, data)
    time.sleep(sleep)


def add_args(data, *args):
    return list(
        map(lambda x: [x[0]] + list(x[1]),
            zip(data, repeat(args)))
    )


test_data = (
    (list(repeat(1, 10)), [1]),
    (list(repeat(2, 10)) + list(repeat(3, 10)) +
     list(repeat(4, 10)), [2, 3, 4]),
)
test_function = (
    run_add_to_list,
    run_binded_add_to_list,
    run_add_to_list_base_class,
)


@pytest.mark.parametrize("function", test_function)
@pytest.mark.parametrize("tested,expected", test_data)
def test_add_to_list(drop_db, run_celery, list_name,
                     tested, expected, function):
    run_in_pool(function, add_args(tested, list_name))
    assert expected == sorted(map(int, get_list(list_name)))


@pytest.mark.parametrize("function", test_function)
def test_add_to_list_many_locks_timeout(drop_db, run_celery,
                                        list_name,  function):
    test_data = list(repeat(5, 10)) + list(repeat(6, 10)) + list(repeat(7, 10))
    run_in_pool(function, add_args(test_data, list_name), sleep=TIMEOUT)
    run_in_pool(function, add_args(test_data, list_name))
    assert [5, 5, 6, 6, 7, 7] == sorted(map(int, get_list(list_name)))
