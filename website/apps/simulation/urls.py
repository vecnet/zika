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
from website.apps.simulation.views.ChartView import ChartView
from website.apps.simulation.views.BrowseView import BrowseView
from website.apps.simulation.views.UploadView import UploadView

urlpatterns = [
    url(r'^$', BrowseView.as_view(), name="simulation.browse"),
    url(r'^upload/', UploadView.as_view(), name="simulation.upload"),
    url(r'^chart/(?P<simulation_id>\d+)/(?P<municipality_code>\d+)/$', ChartView.as_view(), name="simulation.chart"),
]