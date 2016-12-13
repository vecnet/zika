from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'o*4s(hs!!yc3ikl2p9$kftik&hj)#q!&7ey!x&rzjfi4=3jo'

try:
    # Optional settings specific to the local system (for example, custom
    # settings on a developer's system).  The file "settings_local.py" is
    # excluded from version control.
    from .settings_local import *
except ImportError:
    pass
