from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "celeryapp.settings")

app = Celery("celeryapp")

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

"""
@app.task 또는 @shared_task 와 같은
decorator 를 붙여주면,
해당 함수에 대한 API Call 이 들어오는
 순간 Redis 의 Queue 에 해당 작업이 할당됩니다.
Celery 는 할당된 task 들의 순서에 따라 Queue
에 있는 Task 들을 순차적으로 처리합니다.
"""


@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))
    print("hello world")


app.conf.beat_schedule = {
    "add-every-5-seconds": {
        "task": "check_test",
        "schedule": 5.0,
    },
    "add-every-minute-contrab": {
        "task": "data_checking",
        "schedule": crontab(minute=1),
    },
}
