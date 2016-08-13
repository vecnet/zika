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
