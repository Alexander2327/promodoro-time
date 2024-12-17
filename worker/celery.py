from celery import Celery

from core.config import settings

TASKS = [
    'tasks.auth_tasks',
]

celery = Celery(__name__, include=TASKS)
celery.conf.broker_url = settings.celery.broker_url
celery.conf.result_backend = settings.celery.result_backend

# app.autodiscover_tasks(['tasks'], related_name='auth_tasks', force=True)

@celery.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))