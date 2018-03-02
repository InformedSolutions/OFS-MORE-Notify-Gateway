from .base import *

# You should never enable this in production, even if it's temporarily
# All INSTALLED_APPS in django relies on this variable, like google-analytics app.
DEBUG = False

ALLOWED_HOSTS = ['*']

PROD_APPS = [
    'whitenoise',
]

PROD_MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

INSTALLED_APPS = BUILTIN_APPS + THIRD_PARTY_APPS + PROD_APPS + PROJECT_APPS
MIDDLEWARE = MIDDLEWARE + PROD_MIDDLEWARE

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-7*y@^vxedq8a^se_q2_r$6)2)64btin&i(!i0rb&sdgf_-rzy'

# Notify API team-scoped key (sends emails to whitelisted team members)
NOTIFY_API_KEY = "dev_api-7c51af0f-8720-4315-9d67-b4f94d7531e0-df9b0c2e-6d50-4102-ae62-9a24cde656cc"