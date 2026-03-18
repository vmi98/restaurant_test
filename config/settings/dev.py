

try:
    from .base import *  # noqa: F401 F403
except ImportError as e:
    print(f'Import error {e}')

DEBUG = True

ROOT_URLCONF = 'config.urls.dev'

INSTALLED_APPS += [  # noqa: F405
    'debug_toolbar',
]

MIDDLEWARE += [  # noqa: F405
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = [
    '127.0.0.1',
]
