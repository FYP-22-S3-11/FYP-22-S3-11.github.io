from __future__ import absolute_import, unicode_literals
import os
from celery.schedules import crontab
from celery import Celery



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cryptoApi.settings')
app = Celery('cryptoApi')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    "coin_15_sec": {
        "task": "get_list_coin_celery",
        # "schedule": crontab(hour='*/6'),
        "schedule": crontab(minute="*/1"),
        "args": ('test@yopmail.com')
    },
}

# Looks up for task modules in Django applications and loads them
app.autodiscover_tasks()
