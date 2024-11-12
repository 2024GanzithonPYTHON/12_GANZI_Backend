# ganzithon/ganzithon/celery.py
from __future__ import absolute_import, unicode_literals  
import os  
from celery import Celery 

# 기본 Django 설정 모듈 지정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ganzithon.settings')

# Celery 인스턴스 생성
app = Celery('ganzithon')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

