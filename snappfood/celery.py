import os
from celery import Celery
from kombu import Queue

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "snappfood.settings")
app = Celery("snappfood")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


app.conf.task_store_errors_even_if_ignored = True
app.conf.beat_schedule = {}
app.conf.task_default_queue = "default"
app.conf.task_queues = (Queue("default"), )

