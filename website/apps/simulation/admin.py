# Copyright (C) 2016, University of Notre Dame
# All rights reserved


from website.apps.simulation.models import Location, Simulation, Data


from django.contrib import admin

admin.site.register(Location)
admin.site.register(Simulation)
admin.site.register(Data)