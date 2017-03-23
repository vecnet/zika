from django.core.exceptions import ImproperlyConfigured

from .base import *

MANAGERS = (('Alex', 'avyushko@nd.edu'), )
EMAIL_HOST = 'smtp.nd.edu'
EMAIL_PORT = 25
EMAIL_USE_TLS = True

SERVER_EMAIL = "VecNet Zika <vecnet@nd.edu>"
DEFAULT_FROM_EMAIL = "VecNet Zika <vecnet@nd.edu>"

# Supress "You have not set a value for the SECURE_HSTS_SECONDS setting." warning
# Reason: Be sure to read the documentation first; enabling HSTS carelessly can cause serious, irreversible problems.
SILENCED_SYSTEM_CHECKS = ['security.W004', ]

ALLOWED_HOSTS = ['zika.vecnet.org', ]
ADMINS = [('Alex','avyushko@nd.edu'), ('Beth', 'ecaldwe1@nd.edu')
         ]

DEBUG = False

# Security options
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True


# Unless your site should be available over both SSL and non-SSL connections, you may want to either
# set this setting True or configure a load balancer or reverse-proxy server to redirect all connections to HTTPS.
SECURE_SSL_REDIRECT = True

# Set the Anti-MIME-Sniffing header X-Content-Type-Options to 'nosniff'.
# This prevents older versions of Internet Explorer and Chrome from performing MIME-sniffing on the response body,
# potentially causing the response body to be interpreted and displayed as a content type other than the declared
# content type. Current (early 2014) and legacy versions of Firefox will use the declared content type (if one is set),
# rather than performing MIME-sniffing.
SECURE_CONTENT_TYPE_NOSNIFF = True

# Pages will be served with an 'x-xss-protection: 1; mode=block' header to to activate the browser's
# XSS filtering and help prevent XSS attacks
SECURE_BROWSER_XSS_FILTER = True

# VecNet Single Sign On integration
# LOGIN_URL = '/sso/'
# LOGOUT_URL="https://www.vecnet.org/index.php/log-out"
LOGIN_URL = "/auth/login/"
LOGOUT_URL = "/auth/logout/?next=/"

TKT_AUTH_LOGIN_URL = 'https://www.vecnet.org/index.php/sso-login'
TKT_AUTH_PUBLIC_KEY = os.path.join(BASE_DIR, 'apache', 'tkt_pubkey_dsa.pem')

# MIDDLEWARE_CLASSES += ('django_auth_pubtkt.DjangoAuthPubtkt',)

# Enable Google Analytics
DISABLE_GOOGLE_ANALYTICS = False

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },

    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'django.log'),
            'formatter': 'withtimestamp'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'maced_handler': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'mail_admins'],
            'level': 'WARNING',
            'propagate': True,
        },
        'website': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propogate': True,
        },
        'maced': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
    'formatters': {
        'simple': {
           'format': '%(levelname)s: [%(name)s:%(lineno)s] %(message)s'
        },
        'withtimestamp': {
           'format': '%(levelname)s:[%(asctime)s] [%(name)s:%(lineno)s] %(message)s'
        }
    }
}

try:
    # Optional settings specific to the local system (for example, custom
    # settings on a developer's system).  The file "settings_local.py" is
    # excluded from version control.
    from .settings_local import *
except ImportError:
    pass

try:
    # Ignore PyCharm error below if you are using website.settings.dev
    PYTHON_EXECUTABLE
except NameError:
    # Throw an exception if PYTHON_EXECUTABLE is not defined
    raise ImproperlyConfigured("PYTHON_EXECUTABLE option must be defined in settings_local in production environment")

# SECRET_KEY must be defined in settings_local on production environment
# Example:
# SECRET_KEY = 'z5azf=qbb%lmzd^xf9#g5bqtv30e%12P!t(&!0hkpzp0jc8q5$'

# DATABASES must be defined in settings_local in production environment
# PYTHON_EXECUTABLE must be defined in settings_local in production environment
