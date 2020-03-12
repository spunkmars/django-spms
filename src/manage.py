#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    if 'DJANGO_ENV' in os.environ:
        if os.environ['DJANGO_ENV'] == 'prod':
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.prod")
        elif os.environ['DJANGO_ENV'] == 'dev':
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")
        else:
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise

    # This allows easy placement of apps within the interior
    # appxs directory.
    current_path = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.join(current_path, 'appxs'))

    execute_from_command_line(sys.argv)
