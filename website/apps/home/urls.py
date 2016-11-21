#!/bin/env python3.4
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

from website.apps.home.views.DisplaySimulationsView import display_simulations
from website.apps.home.views.MapView import MapView, csv_for_map_view

urlpatterns = [
    # the list of simulations
    url(r'^$', display_simulations, name='home.display_simulations'),

    # get csv data for rendering choropleth map
    url(r'^csv_for_map/(?P<sim_id>[0-9]+)/(?P<inquery_date>[0-9, -]+)/$', csv_for_map_view, name='home.csv_for_map'),

    # views with the choropleth map, whether or not a specific date is supplied
    url(r'^map/(?P<sim_id>[0-9]+)/$', MapView.as_view(), name='home.mapview'),
    url(r'^map/(?P<sim_id>[0-9]+)/(?P<inquery_date>[0-9, -]+)/$', MapView.as_view(), name='home.mapview_with_date'),

]