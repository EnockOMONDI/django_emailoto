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
    'tests',
    'emailoto'
]

ROOT_URLCONF = 'emailoto.urls'
WSGI_APPLICATION = 'tests.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'APP_DIRS': True,
}]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'

EMAILOTO_CONFIG = {
    'redis_host': 'localhost',
    'redis_port': 6379,
    'redis_db': 2,
    'expiration': 1,
    'mailgun_api_key': os.environ.get('MAILGUN_API_KEY'),
    'mailgun_api_url': os.environ.get('MAILGUN_API_URL'),
    'sender': os.environ.get('MAILGUN_SENDER'),
    'template': 'emailoto/default_template.html'
}
