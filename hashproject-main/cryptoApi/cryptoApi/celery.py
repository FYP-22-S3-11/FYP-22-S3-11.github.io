# from __future__ import absolute_import, unicode_literals
# import os
# from celery.schedules import crontab
from celery import Celery

# from django.conf import settings

# # set the default Django settings module for the 'celery' progrom
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cryptoApi.settings')

app = Celery('cryptoApi')

# # configuration obejct to child
# app.config_from_object('django.conf:settings', namespace='CELERY')

# app.autodiscover_tasks()

# app.conf.beat_schedule = {
#     "hash_1_hr": {
#         "task": "hash_scraping",
#         # "schedule": crontab(hour='*/6'),
#         "schedule": crontab(hour="*/1"),
#     },
#     "coin_1_hr": {
#         "task": "coin_scraping",
#         # "schedule": crontab(hour='*/6'),
#         "schedule": crontab(hour="*/1"),
#     },
# }

