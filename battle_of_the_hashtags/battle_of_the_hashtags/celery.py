from __future__ import absolute_import, unicode_literals
import os
from celery import Celery


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'battle_of_the_hashtags.settings')

app = Celery('battle_of_the_hashtags')

REDIS_URL = "redis://localhost:6379/0"

# http://docs.celeryproject.org/en/latest/getting-started/brokers/redis.html#broker-redis
app.conf.broker_url = REDIS_URL

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
