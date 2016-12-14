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
import datetime

from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView

from website.apps.home.models import Location, Data, Simulation
from website.utils.time import datetime_to_unix_timestamp_notz


# @method_decorator(login_required, name='dispatch')
class ChartView(TemplateView):
    template_name = "home/chart.html"

    def get_context_data(self, simulation_id, municipality_code, **kwargs):
        simulation = get_object_or_404(Simulation, id=simulation_id)
        location = get_object_or_404(Location, municipality_code=municipality_code)
        data = Data.objects.filter(simulation=simulation, location=location)
        historical = Data.objects.filter(simulation__historical=1, location=location)

        # Create a time object with the timezone
        time_with_tz = datetime.datetime.min.timetz()

        # Convert each date in the simulation data set to milliseconds
        for d in data:
            date_time = datetime.datetime.combine(d.date, time_with_tz)
            ms_date = datetime_to_unix_timestamp_notz(date_time) * 1000
            d.date = ms_date

        # Convert each date in the historical data set to milliseconds
        for h in historical:
            hist_date_time = datetime.datetime.combine(h.date, time_with_tz)
            ms_hist_date = datetime_to_unix_timestamp_notz(hist_date_time) * 1000
            h.date = ms_hist_date

        # Convert the date the simulation was generated to milliseconds
        sim_gen_date_ms = datetime_to_unix_timestamp_notz(
            datetime.datetime.combine(simulation.date_output_generated, time_with_tz)) * 1000

        context = {
            "location": location,
            "simulation": simulation,
            "data": data,
            "historical_data": historical,
            "sim_generated_date_ms": sim_gen_date_ms
        }

        return context
