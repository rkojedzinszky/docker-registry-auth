"""
Django settings for dra project.
"""

import os
import sys
import socket
import logging

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'change-this')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG') is not None

ALLOWED_HOSTS = ['*'] if DEBUG else os.getenv('ALLOWED_HOSTS', '').split(',')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_atomic_migrations.AtomicMigrations',
    'django_dbconn_retry',
    'dra',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'dra.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'dra.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        # postgresql db with schema support
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DBNAME', 'dra'),
        'HOST': os.getenv('DBHOST', 'postgres'),
        'PORT': os.getenv('DBPORT', '5432'),
        'USER': os.getenv('DBUSER', 'dra'),
        'PASSWORD': os.getenv('DBPASSWORD', 'dra'),
        #'SCHEMA': '',

        'CONN_MAX_AGE': None if os.getenv('DBCONNMAXAGE') == '' else int(os.getenv('DBCONNMAXAGE', '0')),
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

RSA_KEY = os.getenv('RSA_KEY', '/data/key.pem')

DRA_ISS = os.getenv('DRA_ISS', socket.getfqdn())

# Default logging: info and higher messages to stderr
LOGGING = {
    'version': 1,
    'formatters': {
        'default': {
            'format': "%(asctime)s %(levelname)s:%(name)s:%(message)s",
        },
    },
    'handlers': {
        'default': {
            'class': 'logging.StreamHandler',  # sys.stderr is default output
            'stream': sys.stdout,
            'formatter': 'default',
        },
    },
    'root': {
        'level': logging.INFO,
        'handlers': ['default'],
    },
}

try:
    from local_settings import *
except ImportError:
    pass

import sys

if len(sys.argv) > 1 and sys.argv[1] == 'test':
    import tempfile
    RSA_tmpfile = tempfile.NamedTemporaryFile()
    RSA_KEY = RSA_tmpfile.name
    del tempfile

del socket
del sys

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
