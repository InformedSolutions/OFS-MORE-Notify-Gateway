from rest_framework import serializers
from application.models import EmailNotificationRequest, SmsNotificationRequest, Key

#Serializers read request data and validate it against the respective model
class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailNotificationRequest
        fields = ('email', 'templateId', 'personalisation', 'reference')


class SmsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmsNotificationRequest
        fields = ('phoneNumber', 'templateId', 'personalisation', 'reference')


class NotifySerializer(serializers.ModelSerializer):
    class Meta:
        model = Key
        fields = ('apiKey', 'name')