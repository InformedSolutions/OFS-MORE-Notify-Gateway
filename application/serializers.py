from application.models import EmailNotificationRequest, SmsNotificationRequest, Key
from rest_framework import serializers


# Serializers read request data and validate it against the respective model
class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailNotificationRequest
        fields = ('email', 'template_id', 'personalisation', 'reference')


class SmsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmsNotificationRequest
        fields = ('phone_number', 'template_id', 'personalisation', 'reference')


class NotifySerializer(serializers.ModelSerializer):
    class Meta:
        model = Key
        fields = ('api_key', 'name')
