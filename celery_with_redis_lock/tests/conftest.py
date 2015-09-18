import shlex
import subprocess
import time
import os
from itertools import count

import pytest

from example_app.app import get_storage
from example_app.tasks import TIMEOUT

CELERY_CMD = 'celery -A example_app worker --concurrency=4 ' \
             '--loglevel=info -n example_app.%h'


def name_generator(prefix):
    start_time = time.time()
    c = count(0, 1)
    while True:
        yield '%s_%d_%d' % (
            prefix,
            start_time,
            next(c)
        )

list_names = name_generator('list')


@pytest.fixture('module')
def drop_db(request):
    def fin():
        r = get_storage()
        time.sleep(TIMEOUT)
        r.flushdb()
    request.addfinalizer(fin)


@pytest.fixture()
def list_name():
    return next(list_names)


@pytest.fixture(scope='session')
def run_celery(request):
    args = shlex.split(CELERY_CMD)
    chdir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(chdir)
    p = subprocess.Popen(
        args,
        env=os.environ.copy()  # use virtualenv from tox
    )
    time.sleep(2)  # wait for celery

    def fin():
        p.terminate()
    request.addfinalizer(fin)
