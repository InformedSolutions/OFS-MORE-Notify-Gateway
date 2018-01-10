from application.views import send_email, send_sms, change_api_key
from django.conf.urls import url

urlpatterns = [
    # Send Email URL
    url(r'^notify-gateway/api/v1/notifications/email/$', send_email),
    # Send SMS URL
    url(r'^notify-gateway/api/v1/notifications/sms/$', send_sms),
    # Update Notify API Key URL
    url(r'^notify-gateway/api/v1/notifications/api-key/$', change_api_key),
]
