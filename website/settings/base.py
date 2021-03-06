"""
Generated by 'django-admin startproject' using Django 1.8.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Please refer to https://docs.djangoproject.com/en/1.8/ref/contrib/sites/
# for additional information about Django sites framework
SITE_ID = 1

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

ADMINS = (('Alex', 'avyushko@nd.edu'),)

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Although it's not required that you use the sites framework, it's strongly encouraged
    'django.contrib.sites',
    'bootstrap3',
    'rest_framework',
    'website',
    'website.apps.home',
    'website.apps.big_brother',
    'analytics'
    # 'csvimport.app.CSVImportConf'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'website.apps.big_brother.middleware.BigBrotherMiddleware',
    'website.middleware.RedirectionMiddleware',

)

ROOT_URLCONF = 'website.urls'

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
                'django.template.context_processors.static',
                "website.context_processors.app_env"
            ],
        },
    },
]

WSGI_APPLICATION = 'wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# SMTP server configuration
EMAIL_HOST = "smtp.nd.edu"
EMAIL_PORT = 25
EMAIL_USE_TLS = True

# Your project will probably also have static assets that aren't tied to a particular app. In addition to using
# a static/ directory inside your apps, you can define a list of directories (STATICFILES_DIRS) in your settings
# file where Django will also look for static files.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATIC_URL = '/static/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'apache', 'static')

# Absolute filesystem path to the directory that will hold user-uploaded files.
MEDIA_ROOT = os.path.join(BASE_DIR, 'website', 'media')

LOGIN_URL = "/auth/login/"
LOGOUT_URL = "/auth/logout/?next=/"

# Google Analytics is enable in prod environment only
DISABLE_GOOGLE_ANALYTICS = True

# Django logging configuration
# https://docs.djangoproject.com/en/1.8/topics/logging/
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': True,
        },
        'website': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propogate': True,
        }
    },
    "formatters": {
        "simple": {
            "format": "%(levelname)s: [%(name)s:%(lineno)s] %(message)s"
        }
    }
}

# The default is 'SAMEORIGIN', but unless there is a good reason for your site to serve other parts
# of itself in a frame, you should change it to 'DENY'.
# Chart and map are in a frame, so use 'SAMEORIGIN'
X_FRAME_OPTIONS = 'SAMEORIGIN'

DATABASE_BACKUP_DIR = MEDIA_ROOT

# https://docs.djangoproject.com/en/1.10/ref/settings/#data-upload-max-memory-size
# The maximum size in bytes that a request body may be before a SuspiciousOperation (RequestDataTooBig) is raised.
# You can set this to None to disable the check.
DATA_UPLOAD_MAX_MEMORY_SIZE = None
