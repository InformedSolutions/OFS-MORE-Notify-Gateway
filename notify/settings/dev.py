from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

DEV_APPS = [
    'debug_toolbar',
    'django_extensions'
]

MIDDLEWARE_DEV = [
    'debug_toolbar.middleware.DebugToolbarMiddleware'
]

MIDDLEWARE = MIDDLEWARE + MIDDLEWARE_DEV
INSTALLED_APPS = BUILTIN_APPS + THIRD_PARTY_APPS + DEV_APPS + PROJECT_APPS

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'fwzyivx(xxab@bz6g6!v&&qv69mcv^za-vrh@nj5k!61((2aof'

# Notify API development key (does not send real emails)
NOTIFY_API_KEY = "test_key-7c51af0f-8720-4315-9d67-b4f94d7531e0-6ebc794f-f0d9-40c6-bd4f-013119b47c04"