# Copyright (C) 2016, University of Notre Dame
# All rights reserved

from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from website.apps.simulation.models import Location, Data
from website.apps.simulation.models import Simulation


# @method_decorator(login_required, name='dispatch')
class ChartView(TemplateView):
    template_name = "simulation/chart.html"

    def get_context_data(self, simulation_id, location_id, **kwargs):
        simulation = get_object_or_404(Simulation, id=simulation_id)
        location = get_object_or_404(Location, id=location_id)
        data = Data.objects.filter(simulation=simulation, location=location)
        context = {
            "location": location,
            "simulation": simulation,
            "data": data,
        }
        return context
