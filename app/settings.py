"""
Django settings for brain project.

Generated by 'django-admin startproject' using Django 1.11.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os, sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'flnh=1!tsz^4&grtw&0$2&6#n*@aybhg-vdpa-i1rc&pyv$+9c'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',

    'app',
    'device',
    'iot',
    'resource'
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

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'app/templates')
        ],
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

WSGI_APPLICATION = 'app.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'openag_brain',
        'USER': 'openag',
        'PASSWORD': 'openag',
        'HOST': 'localhost',
        'PORT': '',
        'TEST': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'test_openag_brain',
            'USER': 'openag',
            'PASSWORD': 'openag',
        }
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
            'standard_console': {
                'format' : "[%(asctime)s.%(msecs)03d] %(levelname)s %(name)s: %(message)s",
                'datefmt' : "%d/%b/%Y %H:%M:%S"
            },
            'standard_file': {
                'format' : "[%(asctime)s.%(msecs)03d] %(levelname)s %(name)s: %(message)s",
                'datefmt' : "%d/%b/%Y %H:%M:%S"
            },
            'device_console': {
                'format' : "[%(asctime)s.%(msecs)03d] %(levelname)s %(console_name)s: %(message)s",
                'datefmt' : "%d/%b/%Y %H:%M:%S"
            },
            'device_file': {
                'format' : "[%(asctime)s.%(msecs)03d] %(levelname)s %(file_name)s: %(message)s",
                'datefmt' : "%d/%b/%Y %H:%M:%S"
            },
        },
    'handlers': {
        'app_console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard_console',
        },
        'app_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.dirname(BASE_DIR) + "/logs/app.log",
            'formatter': 'standard_file',
        },
        'device_console': { 
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'device_console',
        },
        'device_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.dirname(BASE_DIR) + "/logs/device.log",
            'formatter': 'device_file',
            'maxBytes': 5*1024*1024,
            'backupCount': 1
        },
        'peripheral_files': {
            'level': 'DEBUG',
            'class': 'device.utilities.logger.PeripheralFileHandler',
            'formatter': 'device_file',
        },
        'iot_console': { 
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'device_console',
        },
        'iot_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.dirname(BASE_DIR) + "/logs/iot.log",
            'formatter': 'device_file',
            'maxBytes': 5*1024*1024,
            'backupCount': 1
        },
        'resource_console': { 
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'device_console',
        },
        'resource_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.dirname(BASE_DIR) + "/logs/resource.log",
            'formatter': 'device_file',
            'maxBytes': 5*1024*1024,
            'backupCount': 1
        }
    },
    'loggers': {
        'app': {
            'handlers': ['app_console', 'app_file'],
            'level': 'DEBUG',
        },
        'device': {
            'handlers': ['device_console', 'device_file', 'peripheral_files'],
            'level': 'DEBUG',
        },
        'iot': {
            'handlers': ['iot_console', 'iot_file'],
            'level': 'DEBUG',
        },
        'resource': {
            'handlers': ['resource_console', 'resource_file'],
            'level': 'DEBUG',
        }
    }
}

LOGIN_REDIRECT_URL = 'home'

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

# STATICFILES_DIRS = (os.path.join(BASE_DIR, 'app/static/'))

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "app/static"),
]
STATIC_URL = '/app/static/'
# STATIC_ROOT = "/var/www/example.com/static/"
