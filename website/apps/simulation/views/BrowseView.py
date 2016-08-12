# Copyright (C) 2016, University of Notre Dame
# All rights reserved
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from website.apps.simulation.models import Location
from website.apps.simulation.models import Simulation


# @method_decorator(login_required, name='dispatch')
class BrowseView(TemplateView):
    template_name = "simulation/browse.html"

    def get_context_data(self, **kwargs):
        context = {
            "locations": Location.objects.all(),
            "simulations": Simulation.objects.all(),
        }
        return context
