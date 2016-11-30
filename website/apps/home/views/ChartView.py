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

from website.apps.home.models import Location, Data, Simulation


# @method_decorator(login_required, name='dispatch')
class ChartView(TemplateView):
    template_name = "home/chart.html"

    def get_context_data(self, simulation_id, municipality_code, **kwargs):
        simulation = get_object_or_404(Simulation, id=simulation_id)
        location = get_object_or_404(Location, municipality_code=municipality_code)
        data = Data.objects.filter(simulation=simulation, location=location)
        historical = Data.objects.filter(simulation__historical=1, location=location)

        context = {
            "location": location,
            "simulation": simulation,
            "data": data,
            "historical_data": historical
        }
        return context
