import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'labrin_project.settings')

app = Celery('labrin_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()