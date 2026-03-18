

try:
    from .base import *
except ImportError as e:
    print(f'Import error {e}')

DEBUG = True

ROOT_URLCONF = 'config.urls.dev'

INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = [
    '127.0.0.1',
]