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
        data = Data.objects.filter(simulation=simulation)
        historical = Data.objects.filter(simulation__historical=1)

        totals = sum_cases_by_date(simulation.id, data)
        historical_totals = sum_historical_data(historical)

        # Convert each date in the historical data set to milliseconds
        for h in historical:
            hist_date_time = datetime.datetime.combine(h.date, datetime.datetime.min.time())
            ms_hist_date = datetime_to_unix_timestamp_notz(hist_date_time) * 1000
            h.date = ms_hist_date

        # Convert the date the simulation was generated to milliseconds
        sim_gen_date_ms = datetime_to_unix_timestamp_notz(
            datetime.datetime.combine(simulation.date_output_generated, datetime.datetime.min.time())) * 1000

        context = {
            "simulation": simulation,
            "simulation_mids": totals['mid_totals'],
            "simulation_range": totals['range_totals'],
            "historical_data": historical_totals,
            "sim_generated_date_ms": sim_gen_date_ms
        }

        return context


def sum_cases_by_date(simulation_id, simulation_data):
    date_list = []
    # Get a list of all the dates in the simulation
    for data_point in simulation_data:
        date_list.append(data_point.date)

    # List of unique dates
    date_list = list(set(date_list))
    date_list.sort()

    all_value_mid_totals = []
    all_value_range_totals = []

    for d in date_list:
        sums = Data.objects.filter(simulation_id=simulation_id, date=d).aggregate(total_low_range=Sum('value_low'),
                                                                                  total_mid_point=Sum('value_mid'),
                                                                                  total_high_range=Sum('value_high'))
        date_in_ms = datetime_to_unix_timestamp_notz(datetime.datetime.combine(d, datetime.datetime.min.time())) * 1000

        value_mid_total_for_date = [date_in_ms, sums['total_mid_point']]
        value_range_total_for_date = [date_in_ms, sums['total_low_range'], sums['total_high_range']]

        all_value_mid_totals.append(value_mid_total_for_date)
        all_value_range_totals.append(value_range_total_for_date)

    data_dict = {
        'mid_totals': all_value_mid_totals,
        'range_totals': all_value_range_totals
    }

    return data_dict


def sum_historical_data(historical_data):
    date_list = []
    # Get a list of all the dates in the simulation
    for data_point in historical_data:
        date_list.append(data_point.date)

    # List of unique dates
    date_list = list(set(date_list))
    date_list.sort()

    # List to store totals for each unique date
    all_value_mid_totals = []

    # For each unique date, get the sum for each municipality on that date
    for d in date_list:
        sums = Data.objects.filter(simulation__historical=1, date=d).aggregate(total_mid_point=Sum('value_mid'))

        # Convert dates to milliseconds
        date_in_ms = datetime_to_unix_timestamp_notz(datetime.datetime.combine(d, datetime.datetime.min.time())) * 1000

        # List entry will be date in milliseconds and the sum of all value_mid
        value_mid_total_for_date = [date_in_ms, sums['total_mid_point']]

        all_value_mid_totals.append(value_mid_total_for_date)

    historical_data_totals = all_value_mid_totals

    return historical_data_totals

