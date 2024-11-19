# ganzithon/accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, null=True, blank=True)
    nickname = models.CharField(max_length=100, unique=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    address1 = models.CharField(max_length=100, null=True, blank=True)
    address2 = models.CharField(max_length=100, null=True, blank=True)  
    birthday = models.DateField(null=True, blank=True)  
    current_status = models.CharField(max_length=50, null=True, blank=True)  
    relationship_with_child = models.CharField(max_length=50, null=True, blank=True)  
    child_name = models.CharField(max_length=100, null=True, blank=True)  
