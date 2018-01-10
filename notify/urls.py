from django.conf.urls import url, include

urlpatterns = [
    # Copy URL patterns from app/urls.py
    url(r'^', include('application.urls')),
]
