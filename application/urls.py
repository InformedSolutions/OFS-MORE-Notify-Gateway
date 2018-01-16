"""
OFS-MORE-CCN3: Apply to be a Childminder Beta
-- urls.py --

@author: Informed Solutions
"""

import re

from django.conf import settings
from django.conf.urls import url

from .views import change_api_key, send_email, send_sms

# Configure URL's here
urlpatterns = [
    # Send Email URL
    url(r'^api/v1/notifications/email/$', send_email),
    # Send SMS URL
    url(r'^api/v1/notifications/sms/$', send_sms),
    # Update Notify API Key URL
    url(r'^api/v1/notifications/api-key/$', change_api_key),
]

# Set the URL prefix - currently it's notify-gateway
if settings.URL_PREFIX:
    prefixed_url_pattern = []
    for pat in urlpatterns:
        pat.regex = re.compile(r"^%s/%s" % (settings.URL_PREFIX[1:], pat.regex.pattern[1:]))
        prefixed_url_pattern.append(pat)
    urlpatterns = prefixed_url_pattern
