from celery import Celery

app = Celery('celery_many_producers',
             broker='amqp://guest@localhost//',
             backend='redis://localhost',
             include=['celery_many_producers.tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
)

if __name__ == '__main__':
    app.start()
