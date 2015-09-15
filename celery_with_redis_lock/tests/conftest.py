import pytest

from celery_with_redis_lock.app import LIST_NAME, get_storage


@pytest.fixture()
def drop_list(request):
    def fin():
        r = get_storage()
        print('\n[teardown] remove list')
        r.delete(LIST_NAME)
    request.addfinalizer(fin)
