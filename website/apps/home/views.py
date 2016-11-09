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

from django.views.generic.base import TemplateView
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.template import loader
from django.core.urlresolvers import reverse
import csv
import os
from urllib2 import urlopen
import StringIO

from website.apps.home.models import Location
from website.apps.simulation.models import Data
from website.apps.simulation.models import Simulation
base_dir = os.path.dirname(os.path.abspath(__file__))


class IndexView(TemplateView):
    template_name = "home/index.html"

def dropdown_menu(request, sim_id):
    allinfo = Data.objects.filter(location__municipality_code='05001', simulation_id=sim_id)
    dateinfo = []
    for item in allinfo:
        dateinfo.append(str(item.date))
    print dateinfo

    return render(request, 'home/egcsv.html', {'municipality_code': dateinfo, 'sim_id': sim_id})

def choropleth_map_view(request, inquery_date, sim_id):
    passjspath = reverse('home.csv_for_map', kwargs={"inquery_date": inquery_date, "sim_id": sim_id})
    template = loader.get_template('home/choropleth_map.html')
    context = {'generatefilepath': passjspath, 'inquery_date': inquery_date, 'sim_id': sim_id}
    return HttpResponse(template.render(context, request))

def csv_for_map_view(request, inquery_date, sim_id):
    allinfo = Data.objects.filter(date=inquery_date, simulation_id=sim_id)
    if not allinfo:
        return HttpResponseBadRequest()
    else:
        output = StringIO.StringIO()

        tricky_codes = ['05001', '05002', '05004', '05021', '05030', '05031', '05034', '05036', '05038', '05040', '05042',
                        '05044',
                        '05045', '05051', '05055', '05059', '05079', '05086', '05088', '05091', '05093', '05101', '05107',
                        '05113',
                        '05120', '05125', '05129', '05134', '05138', '05142', '05145', '05147', '05148', '05150', '05154',
                        '05172',
                        '05190', '05197', '05206', '05209', '05212', '05234', '05237', '05240', '05250', '05264', '05266',
                        '05282',
                        '05284', '05306', '05308', '05310', '05313', '05315', '05318', '05321', '05347', '05353', '05360',
                        '05361',
                        '05364', '05368', '05376', '05380', '05390', '05400', '05411', '05425', '05440', '05467', '05475',
                        '05480',
                        '05483', '05490', '05495', '05501', '05541', '05543', '05576', '05579', '05585', '05591', '05604',
                        '05607',
                        '05615', '05628', '05631', '05642', '05647', '05649', '05652', '05656', '05658', '05659', '05660',
                        '05664',
                        '05665', '05667', '05670', '05674', '05679', '05686', '05690', '05697', '05736', '05756', '05761',
                        '05789',
                        '05790', '05792', '05809', '05819', '05837', '05842', '05847', '05854', '05856', '05858', '05861',
                        '05873',
                        '05885', '05887', '05890', '05893', '05895', '08001', '08078', '08137', '08141', '08296', '08372',
                        '08421',
                        '08433', '08436', '08520', '08549', '08558', '08560', '08573', '08606', '08634', '08638', '08675',
                        '08685',
                        '08758', '08770', '08832', '08849']

        writer = csv.writer(output)
        writer.writerow(['ID_ESPACIA', 'value'])
        for data_point in allinfo:
            if data_point.location.municipality_code in tricky_codes:
                data_point.location.municipality_code = data_point.location.municipality_code[1:]
                writer.writerow([data_point.location.municipality_code, data_point.value_mid])
            else:
                writer.writerow([data_point.location.municipality_code, data_point.value_mid])

        return HttpResponse(output.getvalue())

# View for the table of simulations and models
def display_simulations(request):
    simulationinfo = Simulation.objects.all()

    sim_model_list = {}

    simulationlist = {'simulation_id': [], 'model_name': [], 'create_time': []}

    for entry in simulationinfo:
        sim_model_list[entry.id] = entry.model_name
        simulationlist['simulation_id'].append(str(entry.id))
        simulationlist['model_name'].append(entry.model_name)
        simulationlist['create_time'].append(entry.creation_timestamp)

    tests = ["simulation_id", "model_name", "create_time"]
    columns = [simulationlist[test] for test in tests]
    max_len = len(max(columns, key=len))
    for col in columns:
        col += [None]*(max_len-len(col))

    rows = [[col[i] for col in columns] for i in range(max_len)]

    template = loader.get_template('home/simulation.html')
    context = {'simulationlist': sim_model_list, 'simulationlist2': rows, 'tests': tests, }

    return HttpResponse(template.render(context, request))
