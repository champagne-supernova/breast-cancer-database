#--coding: utf-8 --*--
"""
Django settings for bio_database project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@y@96y+vh$=#^)cm!y((5u6c#w@q(@ph9geymqpz=wkdz&*f07'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
	'bio_home',
	'bio_search',
	'bio_genome',
	'bio_publication',
	'bio_reports',
	'bio_expr',
	'bio_go',
	'bio_kegg',
	'bio_microRNA',
	'bio_omic_wiki',
	'bio_variation',
	'bio_homolog'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'bio_database.urls'

WSGI_APPLICATION = 'bio_database.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default':{
	'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'biodb',
        'USER': 'biodb',
        'PASSWORD': 'qwer358!',
        'HOST': '192.168.1.79',
        'PORT': '8000',
    }
}

# DATABASES = {
   # 'default' : {
      # 'ENGINE' : 'django_mongodb_engine',
      # 'NAME' : 'cancer_database'
   # }
# }


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/report/static/'

STATICFILES_DIRS = [
	os.path.join(BASE_DIR, "static"),
]

# Tempaltes directory setting

TEMPLATE_DIRS = (
	os.path.join(BASE_DIR,  'templates'),
)

# Configrate the email

from .email_info import *
EMAIL_USE_TLS = EMAIL_USE_TLS
EMAIL_HOST = EMAIL_HOST
EMAIL_HOST_USER = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD
EMAIL_PORT = EMAIL_PORT

# Log configrations
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
