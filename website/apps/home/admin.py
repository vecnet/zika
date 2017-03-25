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

from django.contrib import admin

from website.apps.home.models import Location, Simulation, Data, SimulationModel, Totals, UploadJob


class LocationAdmin(admin.ModelAdmin):
    list_display = ("id", "department", "department_code", "municipality", "municipality_code", "creation_timestamp")
    ordering = ("department", "municipality")
    search_fields = ("department", "department_code", "municipality", "municipality_code")
admin.site.register(Location, LocationAdmin)

class SimulationAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "disease", "historical", "is_uploaded", "created_by", "creation_timestamp")
    ordering = ("-creation_timestamp",)
    search_fields = ("name", "created_by__username")
admin.site.register(Simulation, SimulationAdmin)

class DataAdmin(admin.ModelAdmin):
    list_display = ("location", "simulation", "value_low", "value_mid", "value_high", "date")
    ordering = ("-simulation",)
    search_fields = ("simulation__name", "location__department", "location__municipality", "simulation__created_by__username")
    list_filter = ("simulation", "location__department")
admin.site.register(Data, DataAdmin)

admin.site.register(Totals)
admin.site.register(SimulationModel)
admin.site.register(UploadJob)
