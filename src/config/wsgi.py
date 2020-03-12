"""
WSGI config for tutorial project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

if 'DJANGO_ENV' in os.environ:
    if os.environ['DJANGO_ENV'] == 'prod':
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.prod")
    elif os.environ['DJANGO_ENV'] == 'dev':
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

application = get_wsgi_application()
