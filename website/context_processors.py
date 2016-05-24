#!/bin/env python2
# -*- coding: utf-8 -*-
#
# This file is part of the VecNet Zika modeling interface.
# For copyright and licensing information about this package, see the
# NOTICE.txt and LICENSE.txt files in its top-level directory; they are
# available at https://github.com/vecnet/zika
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License (MPL), version 2.0.  If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf import settings


def app_env(request):
    """ This function defines login and logout pages.
    If we are running in production enviroment, use auth_pubtkt.
    In dev enviroment, use local django auth system
    """
    env = {"LOGIN_URL": settings.LOGIN_URL,
           "REDIRECT_FIELD_NAME": getattr(settings, 'REDIRECT_FIELD_NAME', 'next'),
           "LOGOUT_URL": settings.LOGOUT_URL}
    # if hasattr(settings, "SERVER_MAINTENANCE_MESSAGE"):
    #      env["SERVER_MAINTENANCE_MESSAGE"] = settings.SERVER_MAINTENANCE_MESSAGE
    return env
