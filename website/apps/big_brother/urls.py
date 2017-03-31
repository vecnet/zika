# Copyright (C) 2016, University of Notre Dame
# All rights reserved

from django.conf.urls import url

from website.database_apps.big_brother.views import tracking_code_view

urlpatterns = [
    url(r"^img/(?P<tracking_code>.*)/$", tracking_code_view, name="big_brother.track"),
]
