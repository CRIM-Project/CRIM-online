# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

SITE_ID = 2

ALLOWED_HOSTS = (
    '127.0.0.1',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'crim.dev.sqlite3',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}

SOLR_SERVER = 'http://localhost:8983/solr/crim'

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240

CORS_ORIGIN_ALLOW_ALL = True

ALLOWED_HOSTS = [
    "crimproject.com",
    "127.0.0.1"
]
CORS_ALLOWED_ORIGINS = [
    "https://crimproject.com",
    "http://127.0.0.1:8000"
]

CORS_ALLOW_METHODS = [
    'GET',
    'OPTIONS',
]

# This value is a placeholder for development
SECRET_KEY = "development.environment"

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
    },
    # 'highlights': {
    #     'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
    #     'LOCATION': '/Users/jchthys/crim-cache-highlights',
    #     'OPTIONS': {
    #         'MAX_ENTRIES': 12000,
    #     },
    #     'TIMEOUT': None,
    # },
}

INTERNAL_IPS = [
    # ...
    '127.0.0.1',
    # ...
]

# This value is a placeholder for development of the application
ADMIN_EMAIL = 'development@crimonline.org'

