from django.conf import settings


def global_settings(request):
    return {
        'SITE_NAME': settings.SITE_NAME,
        'SITE_DESC': settings.SITE_DESC,
        'SITE_VERSION': settings.SITE_VERSION,
        'SITE_COPYRIGHT_YEAR': settings.SITE_COPYRIGHT_YEAR,
    }
