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
from django.db.models import Sum

from website.apps.home.models import Location, Data, Simulation, Totals
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
        time_no_tz = datetime.datetime.min.time()

        # Convert each date in the simulation data set to milliseconds
        for d in data:
            date_time = datetime.datetime.combine(d.date, time_no_tz)
            ms_date = datetime_to_unix_timestamp_notz(date_time) * 1000
            d.date = ms_date

        # Convert each date in the historical data set to milliseconds
        for h in historical:
            hist_date_time = datetime.datetime.combine(h.date, time_no_tz)
            ms_hist_date = datetime_to_unix_timestamp_notz(hist_date_time) * 1000
            h.date = ms_hist_date

        # Convert the date the simulation was generated to milliseconds
        sim_gen_date_ms = datetime_to_unix_timestamp_notz(
            datetime.datetime.combine(simulation.date_output_generated, time_no_tz)) * 1000

        context = {
            "location": location,
            "simulation": simulation,
            "data": data,
            "historical_data": historical,
            "sim_generated_date_ms": sim_gen_date_ms,
        }

        return context


# @method_decorator(login_required, name='dispatch')
class CountryTotalChartView(TemplateView):
    template_name = "home/country_total_chart.html"

    def get_context_data(self, simulation_id, **kwargs):
        simulation = get_object_or_404(Simulation, id=simulation_id)
        totals_data = Totals.objects.filter(simulation=simulation)
        historical_totals_data = Totals.objects.filter(simulation__historical=1)

        data_dict = format_totals_by_date(totals_data)
        historical_data = format_historical_totals(historical_totals_data)

        # Convert the date the simulation was generated to milliseconds
        sim_gen_date_ms = datetime_to_unix_timestamp_notz(
            datetime.datetime.combine(simulation.date_output_generated, datetime.datetime.min.time())) * 1000

        context = {
            "simulation": simulation,
            "simulation_mids": data_dict['mid_totals'],
            "simulation_range": data_dict['range_totals'],
            "historical_data": historical_data,
            "sim_generated_date_ms": sim_gen_date_ms
        }

        return context


def format_totals_by_date(totals_data):
    # Sort data list by date
    sorted_totals_data = sorted(totals_data, key=lambda total: total.data_date)

    all_value_mid_totals = []
    all_value_range_totals = []

    for total_obj in sorted_totals_data:
        date_in_ms = datetime_to_unix_timestamp_notz(datetime.datetime.combine(total_obj.data_date, datetime.datetime.min.time())) * 1000

        value_mid_total_for_date = [date_in_ms, total_obj.total_mid]
        all_value_mid_totals.append(value_mid_total_for_date)

        value_range_total_for_date = [date_in_ms, total_obj.total_low, total_obj.total_high]
        all_value_range_totals.append(value_range_total_for_date)

    data_dict = {
        'mid_totals': all_value_mid_totals,
        'range_totals': all_value_range_totals
    }

    return data_dict


def format_historical_totals(historical_totals_data):
    # Sort data list by date
    sorted_totals_data = sorted(historical_totals_data, key=lambda total: total.data_date)

    all_value_mid_totals = []

    # For each unique date, get the sum for each municipality on that date
    for total_obj in sorted_totals_data:
        date_in_ms = datetime_to_unix_timestamp_notz(
            datetime.datetime.combine(total_obj.data_date, datetime.datetime.min.time())) * 1000

        value_mid_total_for_date = [date_in_ms, total_obj.total_mid]
        all_value_mid_totals.append(value_mid_total_for_date)

    return all_value_mid_totals

