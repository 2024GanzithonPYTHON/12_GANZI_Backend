# ganzithon/purchase/models.py
from django.db import models
from accounts.models import CustomUser
from django.utils import timezone
from datetime import datetime

class PurchasePost(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    image = models.URLField(null=True, blank=True)  # 이미지 URL을 위한 필드
    tags = models.JSONField(null=True, blank=True)  # 선택 사항: JSON 형식으로 태그 저장
    body = models.TextField()
    email_subject = models.CharField(max_length=100)
    email_body = models.TextField()
    payment_period = models.DateField()
    bank_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=200)
    contact_info = models.CharField(max_length=200)
    duration_date = models.DateField()
    duration_time = models.TimeField()
    min_participants = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def duration(self):
        combined_datetime = datetime.combine(self.duration_date, self.duration_time)
        return timezone.make_aware(combined_datetime, timezone.get_current_timezone())
