# Copyright (C) 2016, University of Notre Dame
# All rights reserved


from django.conf.urls import url
from website.apps.simulation.views.ChartView import ChartView
from website.apps.simulation.views.BrowseView import BrowseView
from website.apps.simulation.views.UploadView import UploadView

urlpatterns = [
    url(r'^$', BrowseView.as_view(), name="simulation.browse"),
    url(r'^upload/', UploadView.as_view(), name="simulation.upload"),
    url(r'^chart/(?P<simulation_id>\d+)/(?P<location_id>\d+)/$', ChartView.as_view(), name="simulation.chart"),
]