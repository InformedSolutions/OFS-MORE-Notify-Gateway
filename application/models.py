from django.contrib.postgres.fields.jsonb import JSONField
from django.db import models


class EmailNotificationRequest(models.Model):
    # Email Data validation rules
    email = models.CharField(max_length=100, blank=False)
    template_id = models.UUIDField(blank=False)
    reference = models.CharField(max_length=100, blank=True, default='')
    personalisation = JSONField(blank=True)


class SmsNotificationRequest(models.Model):
    # Phone Number validation rules
    phone_number = models.CharField(max_length=11, blank=False)
    template_id = models.UUIDField(blank=False)
    reference = models.CharField(max_length=100, blank=True, default='')
    personalisation = JSONField(blank=True)


class Key(models.Model):
    # API key validation rules
    # Name is a placeholder as there needs to be more than one entry to execute without error
    name = models.CharField(max_length=100, blank=True)
    api_key = models.CharField(max_length=100, blank=False)
