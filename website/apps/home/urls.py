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
from website.apps.home.views import load_municipality

from website.apps.home.views import testchoropleth
from website.apps.home.views import load_examplecsv
from website.apps.home.views import dropdown_menu
from website.apps.home.views import detailchoropleth
from website.apps.home.views import csvfake


urlpatterns = [

    url(r'^testchoropleth/$', testchoropleth, name='choropleth_map'),
    url(r'^loadexamplecsv/$', load_examplecsv),

    # hard to get to this page
    url(r'^municipality/(?P<department_name>[A-Z, a-z, _]+)/(?P<municipality_name>[A-Z, a-z, _]+)/$', load_municipality),

    url(r'^dropdnegcsv/$', dropdown_menu, name='home.dropdown'),

    # just choropleth map and highchart
    url(r'^choroplethdetail/(?P<inquery_date>[0-9, -]+)/$', detailchoropleth),

    url(r'^csvfake/(?P<inquery_date>[0-9, -]+)/$', csvfake, name='csvfake'),

    # department infor using highchart, example: http://127.0.0.1:8000/home/CESAR/
    url(r'^(?P<department_name>[A-Z, a-z, _]+)/$', load_locations),
]