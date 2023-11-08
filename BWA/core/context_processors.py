from django.conf import settings


def selected_settings(request):
    return {'APP_VERSION_NUMBER': settings.APP_VERSION_NUMBER,
            'GED_MAX_FILE_SIZE': settings.GED_MAX_FILE_SIZE,
            'GED_ALLOWED_EXTENSION_FILE': settings.GED_ALLOWED_EXTENSION_FILE
            }
