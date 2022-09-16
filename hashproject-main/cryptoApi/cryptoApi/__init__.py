from __future__ import absolute_import
from .celery_app import app as celery_app
import pymysql

default_app_config = 'api.apps.ApiConfig'

__all__ = ['celery_app']
pymysql.install_as_MySQLdb()