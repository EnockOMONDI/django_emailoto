import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = 'obviously-not-a-production-secret'
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tests'
]

ROOT_URLCONF = 'tests.urls'
WSGI_APPLICATION = 'tests.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'

EMAILOTO_REDIS_HOST = os.environ.get('REDIS_HOST')
EMAILOTO_REDIS_PORT = os.environ.get('REDIS_PORT')
EMAILOTO_REDIS_DB = os.environ.get('REDIS_DB')
EMAILOTO_REDIS_KEY_EXPIRATION = 1
