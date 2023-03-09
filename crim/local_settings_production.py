# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

SITE_ID = 2

ALLOWED_HOSTS = (
    '127.0.0.1',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'crimdata'
    }
}

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

SOLR_SERVER = 'http://localhost:8983/solr/crim'

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_METHODS = [
    'GET',
    'OPTIONS',
]

SECRET_KEY = "changeme"

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '~/crim-cache-default/',
        'OPTIONS': {
            'MAX_ENTRIES': 6000,
        },
        'TIMEOUT': None,
    },
    'pieces': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '~/crim-cache-pieces',
        'OPTIONS': {
            'MAX_ENTRIES': 6000,
        },
        'TIMEOUT': None,
    },
    'observations': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '~/crim-cache-observations',
        'OPTIONS': {
            'MAX_ENTRIES': 600000,
        },
        'TIMEOUT': None,
    }
}

INTERNAL_IPS = [
    '127.0.0.1',
]

ADMIN_EMAIL = 'changeme'