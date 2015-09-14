celery_many_producers
=====================

Experimenting with Redis.lock under Celery

Usage
-----
Install dependencies:
    pip install tox celery

Run celery:
    celery -A celery_many_producers worker --concurrency=4 --loglevel=info -n celery_many_producers.%h

Run tests:
    tox -r

Licence
-------

http://www.wtfpl.net/txt/copying/

Authors
-------

`celery_many_producers` was written by `Mateusz Pro. <mateusz.probachta@gmail.com>`_.
