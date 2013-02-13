from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'chaos',
        'USER': 'chaos',
        'PASSWORD': 'chaos',
        'HOST': 'localhost',
        'PORT': '',
    }
}

TIME_ZONE = 'Europe/Moscow'
LANGUAGE_CODE = 'ru'

INSTALLED_APPS += (
    'debug_toolbar',
)
MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
INTERNAL_IPS = ('127.0.0.1')
