import os

if 'DJANGO_ENV' in os.environ:
    if os.environ['DJANGO_ENV'] == 'prod':
        from .prod import *
    elif os.environ['DJANGO_ENV'] == 'dev':
        from .dev import *
    elif os.environ['DJANGO_ENV'] == 'local':
        from .local import *
    else:
        from .local import *
else:
    from .local import *
