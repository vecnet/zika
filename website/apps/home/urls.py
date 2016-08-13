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

from django.conf.urls import url
from website.apps.home.views import load_locations
from website.apps.home.views import testview
from website.apps.home.views import testmap

urlpatterns = [
    #url(r'^$', testview),
    url(r'^$', testmap),
    url(r'^(?P<department_name>[A-Z, a-z, _]+)/$', load_locations),
]