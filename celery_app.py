from celery import Celery


celery_app = Celery('xtceleryapp',
                    broker='amqp://admin:admin@localhost/',
                    backend='redis://localhost:6379/1')

celery_app.conf.update(task_track_started=True)
