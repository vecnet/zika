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
from website.apps.data_browser.views import hello
from website.apps.data_browser.views import location_list
from website.apps.data_browser.views import location_info
from website.apps.data_browser.views import location_info_chart
from website.apps.data_browser.views import testchart
from website.apps.data_browser.views import getlocationinfo

urlpatterns = [
    url(r'^$', location_list),
    url(r'^test/', testchart),
    url(r'^detail/(?P<municipality_code>[0-9]+)/$', getlocationinfo),
    url(r'^(?P<hello_id>[0-9]+)/$', hello),
    url(r'^(?P<query_location>[A-Z, a-z, -]+)/$', location_info),
    url(r'^chart/(?P<chart_location>[A-Z, a-z, -]+)/$', location_info_chart),
]
