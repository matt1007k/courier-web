"""
Django settings for courier_app project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*65*l=b#857p)4o=v2@-0(%jr7hoex=igo$ojzw^n2f$kxv+_w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'livereload',
    'django_inlinecss',
    'rest_framework',
    'channels',
    'qr_code',

    'pages',
    'authentication',
    'drivers',
    'clients',
    'orders',
    'addresses',
    'details',
    'valorations',
    'promo_codes',
    'service_prices',
    'driver_payments',
    'settings'
]

# INSTALLED_APPS += ('naomi',)


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'livereload.middleware.LiveReloadScript',
]

ROOT_URLCONF = 'courier_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'courier_app.admin_context.menu_items',
            ],
        },
    },
]

WSGI_APPLICATION = 'courier_app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'es-pe'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'America/Lima'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_ROOT = BASE_DIR.joinpath('static')
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR.joinpath('courier_app/static')
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR.joinpath('media')

AUTH_USER_MODEL = 'authentication.User'

AUTHENTICATION_BACKENDS = ['authentication.backends.EmailBackend']

# LOGIN_REDIRECT_URL = '/auth/login'
LOGIN_URL = '/auth/login'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
}

# Real time
ASGI_APPLICATION = 'courier_app.asgi.application'
# 
# Cache with redis
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}


from decouple import config

EMAIL_HOST = 'smtp.googlemail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'mattfor17@gmail.com'
EMAIL_HOST_PASSWORD = config('USER_MAIL_PASSWORD')
EMAIL_USE_TLS = True

# if DEBUG:
#     EMAIL_BACKEND = "naomi.mail.backends.naomi.NaomiBackend"
#     EMAIL_FILE_PATH = "/mnt/c/Users/nomad1007/Documents/Code/courier-web/mailtest/tmp"


try:
    from .local_settings import *
except ImportError:
    pass
