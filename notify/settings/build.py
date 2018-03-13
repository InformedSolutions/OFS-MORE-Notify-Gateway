from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

MIDDLEWARE_DEV = [
    'debug_toolbar.middleware.DebugToolbarMiddleware'
]

MIDDLEWARE = MIDDLEWARE + MIDDLEWARE_DEV
INSTALLED_APPS = BUILTIN_APPS + THIRD_PARTY_APPS + PROJECT_APPS

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'bwf1%fz)rl&i7zb9hd$bkccqw-402hq=mg=h*31(w=@b+iz-8*'

NOTIFY_API_KEY = os.environ.get('NOTIFY_API_KEY')