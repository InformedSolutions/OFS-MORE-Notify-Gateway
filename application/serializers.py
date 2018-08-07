"""
Serializer functions for notify domain models
"""

from rest_framework import serializers

from .models import EmailNotificationRequest, ApiKey, SmsNotificationRequest


# Serializers read request data and validate it against the respective model
class EmailSerializer(serializers.ModelSerializer):
    """
    Initializing the email serializer so that we can validate data against the model.
    This data is not stored in a database, but is instead immediately forwarded onto GOV UK Notify after validation.
    """

    class Meta:
        model = EmailNotificationRequest
        fields = ('service_name', 'email', 'template_id', 'personalisation', 'reference')


class SmsSerializer(serializers.ModelSerializer):
    """
    Initializing the sms serializer so that we can validate data against the model.
    This data is not stored in a database, but is instead immediately forwarded onto GOV UK Notify after validation.
    """

    class Meta:
        model = SmsNotificationRequest
        fields = ('service_name', 'phone_number', 'template_id', 'personalisation', 'reference')


class NotifySerializer(serializers.ModelSerializer):
    """
    Initializing the serializer for updating the api key.  This data is simply validated then stored in a variable
    """

    class Meta:
        model = ApiKey
        fields = ('api_key',)
