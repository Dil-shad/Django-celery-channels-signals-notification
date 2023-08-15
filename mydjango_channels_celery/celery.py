from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings
from celery.schedules import crontab

# from django_celery_beat.models import PeriodicTask


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mydjango_channels_celery.settings")

app = Celery('celery_django')
app.conf.enable_utc = False
app.conf.update(timezone='Asia/Kolkata')
app.config_from_object('django.conf:settings', namespace='CELERY')


# celery Beat settings
app.conf.beat_schedule = {
    'counter_task': {
        'task': 'mainapp.tasks.test_functions',
        'schedule': crontab(hour=11, minute=7),
        'args': (['10'],)  
    } 
}
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}') 


