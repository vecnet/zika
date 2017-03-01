import sys

from django.core.exceptions import ImproperlyConfigured

from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'o*4s(hs!!yc3ikl2p9$kftik&hj)#q!&7ey!x&rzjfi4=3jo'

# Note sys.executable only works with Django debug server
# It has no meaning when running in mod_wsgi environment
PYTHON_EXECUTABLE = sys.executable

try:
    # Optional settings specific to the local system (for example, custom
    # settings on a developer's system).  The file "settings_local.py" is
    # excluded from version control.
    from .settings_local import *
except ImportError:
    pass
