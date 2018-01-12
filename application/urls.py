import re
from application.views import send_email, send_sms, change_api_key
from django.conf.urls import url

from django.conf import settings

urlpatterns = [
    # Send Email URL
    url(r'^api/v1/notifications/email/$', send_email),
    # Send SMS URL
    url(r'^api/v1/notifications/sms/$', send_sms),
    # Update Notify API Key URL
    url(r'^api/v1/notifications/api-key/$', change_api_key),
]

if settings.URL_PREFIX:
    prefixed_url_pattern = []
    for pat in urlpatterns:
        pat.regex = re.compile(r"^%s/%s" % (settings.URL_PREFIX[1:], pat.regex.pattern[1:]))
        prefixed_url_pattern.append(pat)
    urlpatterns = prefixed_url_pattern
