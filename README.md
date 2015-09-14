# celery_with_redis_lock

Experimenting with Redis.lock under Celery

## Usage

Install dependencies:
```bash
pip install tox celery
```

Run celery:
```bash
celery -A celery_with_redis_lock worker --concurrency=4 --loglevel=info -n celery_with_redis_lock.%h
```

Run tests:
```bash
tox -r
```

## Licence
http://www.wtfpl.net/txt/copying/

## Authors
`celery_with_redis_lock` was written by `Mateusz Pro. <mateusz.probachta@gmail.com>`_.
