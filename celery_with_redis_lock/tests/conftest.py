import pytest

from celery_with_redis_lock.app import LIST_NAME, get_storage


@pytest.fixture()
def drop_db(request):
    def fin():
        r = get_storage()
        r.flushdb()
    request.addfinalizer(fin)
