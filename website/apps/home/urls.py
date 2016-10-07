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
#from website.apps.home.views import load_municipality

from website.apps.home.views import dropdown_menu
from website.apps.home.views import choropleth_map_view
from website.apps.home.views import csv_for_map_view


urlpatterns = [
    url(r'^$', dropdown_menu, name='home.dropdown'),

    # hard to get to this page
    # url(r'^municipality/(?P<department_name>[A-Z, a-z, _]+)/(?P<municipality_name>[A-Z, a-z, _]+)/$', load_municipality),

    # just choropleth map and highchart
    url(r'^choropleth_map/(?P<inquery_date>[0-9, -]+)/$', choropleth_map_view, name="choropleth_map"),

    url(r'^csv_for_map/(?P<inquery_date>[0-9, -]+)/$', csv_for_map_view, name='csv_for_map'),

    # department infor using highchart, example: http://127.0.0.1:8000/home/CESAR/
    url(r'^(?P<department_name>[A-Z, a-z, _]+)/$', load_locations),
]