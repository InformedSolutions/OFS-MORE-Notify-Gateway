from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

MIDDLEWARE_DEV = [
    'debug_toolbar.middleware.DebugToolbarMiddleware'
]

MIDDLEWARE = MIDDLEWARE + MIDDLEWARE_DEV
INSTALLED_APPS = BUILTIN_APPS + THIRD_PARTY_APPS + PROJECT_APPS
