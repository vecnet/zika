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

from website.apps.home.views.upload_job_view import upload_job_view
from website.apps.home.views.BrowseView import ListModelView
from website.apps.home.views.ChartView import ChartView, CountryTotalChartView
from website.apps.home.views.MapView import MapView, csv_for_map_view
from website.apps.home.views.UploadView import UploadView
from website.apps.home.views.delete_simulation_view import delete_simulation_view

urlpatterns = [
    # the list of simulations
    url(r'^list/$', ListModelView.as_view(), name='home.list_view'),
    url(r'^historical/$', ListModelView.as_view(), kwargs={"is_historical":True}, name='home.display_historical'),

    # upload simulation/historical data view
    url(r'^upload/', UploadView.as_view(), name="simulation.upload"),

    # get csv data for rendering choropleth map
    url(r'^csv_for_map/(?P<sim_id>[0-9]+)/(?P<inquery_date>[0-9, -]+)/$', csv_for_map_view, name='home.csv_for_map'),

    # views for the charts (country totals or municipality)
    url(r'^chart/(?P<simulation_id>\d+)/total/$', CountryTotalChartView.as_view(), name='home.countrytotalchart'),
    url(r'^chart/(?P<simulation_id>\d+)/(?P<municipality_code>\d+)/$', ChartView.as_view(), name="simulation.chart"),

    # Permanently delete simulation
    url(r'^delete/(?P<simulation_id>\d+)/$', delete_simulation_view, name="simulation.delete"),

    # views for the map
    url(r'^map/(?P<model_id>[0-9]+)/(?P<sim_id>[0-9]+)/$', MapView.as_view(), name='home.mapview'),
    url(r'^map/(?P<model_id>[0-9]+)/(?P<sim_id>[0-9]+)/(?P<municipality_code>\d+)/$',
        MapView.as_view(), name='home.mapview'),

    # API
    url(r'^api/upload_job/(?P<pk>\d+)/$', upload_job_view, name="api.upload_job"),
]
