"""
Django settings for calctmenu project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from decouple import config, Csv

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = '5hwz_md$cu=+3sdm4*%c4#s5+p&^t26ntxz$+-i2c5wr6)-8qc'
SECRET_KEY = config('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = config('DJANGO_DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

INTERNAL_IPS = [
    '127.0.0.1',
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.novedades',
    'apps.calculadora',
    'bootstrapform',
    'phonenumber_field',
    'file_resubmit',
    'debug_toolbar',
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

MIDDLEWARE_CLASSES = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
    "file_resubmit": {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        "LOCATION": '/tmp/file_resubmit/'
    }
}

ROOT_URLCONF = 'calctmenu.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'calctmenu.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'es-ar'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# 
AUTH_USER_MODEL = 'calculadora.User'

# This is the default backend. Email will be sent through a SMTP server.
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# This URL is redirected to login.html when the user wants to identify himself
LOGIN_URL = '/sign-in/'

# This URL redirect to the home page after user is signin
LOGIN_REDIRECT_URL = 'calculadora:home'

# This URL redirect to the home paga after user is logout
LOGOUT_REDIRECT_URL = 'calculadora:home'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

# AWS Settings
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN =  config('AWS_S3_CUSTOM_DOMAIN') % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

# AWS Static Settings
AWS_STATIC_LOCATION = 'static'

# STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_STATIC_LOCATION)
# STATICFILES_STORAGE = 'storage_backends.StaticStorage'

# This lists additional directories that Django's collectstatic
#  tool should search for static files
# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# The absolute path to the directory where collectstatic will 
# collect static files for deployment
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# The URL to use when referring to static files (where they
# will be served from)
STATIC_URL = '/static/'

# AWS Public Media Settings
AWS_PUBLIC_MEDIA_LOCATION = 'media'

# The URL to use when referring to media files (where they
# will be served from)
MEDIA_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_PUBLIC_MEDIA_LOCATION)

DEFAULT_FILE_STORAGE =  'storage_backends.PublicMediaStorage'

# AWS Private Media Settings
AWS_PRIVATE_MEDIA_LOCATION = 'private'
PRIVATE_FILE_STORAGE =  'storage_backends.PrivateMediaStorage'

DEFAULT_FILES_STORAGE = 'storage_backends.PublicMediaStorage'

# The absolute path to the directory where will storage the media 
# files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Heroku: Update database configuration from $DATABASE_URL
import dj_database_url

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)