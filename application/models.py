"""
Model definitions for notify domain models
"""

from django.contrib.postgres.fields.jsonb import JSONField
from django.db import models


class EmailNotificationRequest(models.Model):
    """
    This is where the notify-gateway validation rules are set for email requests
    """
    service_name = models.CharField(blank=True)
    email = models.CharField(max_length=100, blank=False)
    template_id = models.UUIDField(blank=False)
    reference = models.CharField(max_length=100, blank=True, default='')
    personalisation = JSONField(blank=True)


class SmsNotificationRequest(models.Model):
    """
    This is where the notify-gateway validation rules are set for sms requests
    """
    phone_number = models.CharField(max_length=11, blank=False)
    template_id = models.UUIDField(blank=False)
    reference = models.CharField(max_length=100, blank=True, default='')
    personalisation = JSONField(blank=True)


class ApiKey(models.Model):
    """
    This is where the notify-gateway validation rules are set for api-key update requests
    """
    api_key = models.CharField(max_length=100, blank=False)
