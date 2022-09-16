from __future__ import absolute_import, unicode_literals
import os
from celery.schedules import crontab
from celery import Celery

from django.conf import settings

print("---------celery called")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cryptoApi.settings')
app = Celery('cryptoApi')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    "coin_15_sec": {
        "task": "api.tasks.get_list_coin_celery_demo",
        # "schedule": crontab(hour='*/6'),
        "schedule": crontab(minute="*/1"),
        # "args": ('test@yopmail.com')
    },
    'create-file-ten-seconds': {
        # Task Name (Name Specified in Decorator)
        'task': 'create_file',  
        # Schedule      
        'schedule': 10.0,
        # Function Arguments 
        'args': ("Hello",) 
    },
}

app.conf.task_routes = {
#     "account.tasks.test_task_job": {
#         "queue": "celery"
#     },
    "api.task.get_list_coin_celery_demo": {
        "queue": "celery"
    },
}

app.conf.accept_content = settings.CELERY_ACCEPT_CONTENT
app.conf.task_serializer = settings.CELERY_TASK_SERIALIZER
app.conf.result_serializer = settings.CELERY_RESULT_SERIALIZER
app.conf.worker_prefetch_multiplier = \
    settings.CELERY_WORKER_PREFETCH_MULTIPLIER
# To restart worker processes after every task
app.conf.broker_url = settings.BROKER_URL
app.conf.broker_transport_options = settings.BROKER_TRANSPORT_OPTIONS
app.conf.result_backend = settings.CELERY_RESULT_BACKEND

# Looks up for task modules in Django applications and loads them
app.autodiscover_tasks()
