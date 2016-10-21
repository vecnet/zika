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
from django.http.response import HttpResponse
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


def testview(request):
    allfile = [
        #"Municipality_Zika_2016-01-09.csv", "Municipality_Zika_2016-01-16.csv",
        #"Municipality_Zika_2016-01-23.csv", "Municipality_Zika_2016-01-30.csv",
        #"Municipality_Zika_2016-02-06.csv", "Municipality_Zika_2016-02-13.csv",
        #"Municipality_Zika_2016-02-20.csv", "Municipality_Zika_2016-02-27.csv",
        #"Municipality_Zika_2016-03-05.csv", "Municipality_Zika_2016-03-12.csv",
        #"Municipality_Zika_2016-03-19.csv", "Municipality_Zika_2016-03-26.csv",
        #"Municipality_Zika_2016-04-02.csv", "Municipality_Zika_2016-04-09.csv",
        #"Municipality_Zika_2016-04-16.csv", "Municipality_Zika_2016-04-23.csv",
        #"Municipality_Zika_2016-04-30.csv", "Municipality_Zika_2016-05-07.csv",
        #"Municipality_Zika_2016-05-14.csv", "Municipality_Zika_2016-05-21.csv",
        #"Municipality_Zika_2016-05-28.csv", "Municipality_Zika_2016-06-04.csv",
        #"Municipality_Zika_2016-06-11.csv", "Municipality_Zika_2016-06-18.csv",
        #"Municipality_Zika_2016-06-25.csv", "Municipality_Zika_2016-07-02.csv",
        #"Municipality_Zika_2016-07-09.csv", "Municipality_Zika_2016-07-16.csv"
    ]

    filename = []

    for item in allfile:
        csvpath = "https://raw.githubusercontent.com/cdcepi/zika/master/Colombia/Municipality_Zika/data/" + item
        filename.append(csvpath)

    for item in filename:
        webpage = urlopen(item)
        codereader = csv.reader(webpage, delimiter=',', quotechar='"')

        for row in codereader:
            if row[0] != 'report_date':
                locationitem = Location()
                locationitem.report_date = row[0]
                locationitem.location = row[1]
                locationitem.department = row[1].split('-')[1]
                locationitem.municipality = row[1].split('-')[2]
                locationitem.data_type = row[3]
                locationitem.data_field_code = row[4]
                if row[7] == 'NA':
                    locationitem.value = 0
                else:
                    locationitem.value = row[7]
                locationitem.save()

    return HttpResponse(content="success")


def load_locations(request, department_name, chartID='chartID'):
    chart_department = department_name[0]+department_name[1:].lower()
    department_name = department_name[:-11]
    print chart_department

    dateseries = []
    dateseries1 = {'dates':[], }
    datac1 = Location.objects.filter(data_field_code='CO0001', department=chart_department)
    countc1 = []
    countc2 = []
    countc3 = []
    countc4 = []

    for item in datac1:
        if item.report_date not in dateseries:
            dateseries.append(item.report_date)
    print dateseries

    for item in dateseries:
        datac1 = Location.objects.filter(report_date=item, department=chart_department, data_field_code='CO0001')
        datac2 = Location.objects.filter(report_date=item, department=chart_department, data_field_code='CO0002')
        datac3 = Location.objects.filter(report_date=item, department=chart_department, data_field_code='CO0003')
        datac4 = Location.objects.filter(report_date=item, department=chart_department, data_field_code='CO0004')
        countco001 = 0
        countco002 = 0
        countco003 = 0
        countco004 = 0
        for item in datac1:
            countco001 += item.value
        countc1.append(countco001)
        for item in datac2:
            countco002 += item.value
        countc2.append(countco002)
        for item in datac3:
            countco003 += item.value
        countc3.append(countco003)
        for item in datac4:
            countco004 += item.value
        countc4.append(countco004)
    print countc1

    for item in dateseries:
        dateseries1['dates'].append(item.strftime('%y/%m/%d'))
    print dateseries1

    chart_title = "customized line style with data from local database"

    chart = {"renderTo": chartID, "type": 'spline', "height": '500',}
    title = {"text": str(chart_title)}
    xAxis = {"title": {"text": 'Dates'}, "categories": dateseries1['dates']}
    yAxis = {"title": {"text": 'Cases'}}

    series = [
        {"name": 'zika_confirmed_laboratory', "data": countc1, "zoneAxis": 'x', "zones": [{"value": 8}, {"dashStyle": 'dot'}]},
        #{"name": 'zika_confirmed_clinic', "data": countc2},
        {"name": 'zika_suspected', "data": countc3, "zoneAxis": 'x', "zones": [{"value": 8}, {"dashStyle": 'dot'}]},
        #{"name": 'zika_suspected_clinic', "data": countc4},
    ]

    return render(request, 'home/departmentchart.html', {'chartID': chartID, 'chart': chart, 'series': series,
                                                        'title': title, 'xAxis': xAxis, 'yAxis': yAxis,
                                                        'chart_title': chart_title, 'department_name': chart_department})


def dropdown_menu(request, sim_id):
    allinfo = Data.objects.filter(location__municipality_code='05001', simulation_id=sim_id)
    dateinfo = []
    for item in allinfo:
        dateinfo.append(str(item.date))
    print dateinfo

    return render(request, 'home/egcsv.html', {'municipality_code': dateinfo, 'sim_id': sim_id},)


def choropleth_map_view(request, inquery_date, sim_id):
    passjspath = reverse('csv_for_map', kwargs={"inquery_date": inquery_date, "sim_id": sim_id,})
    template = loader.get_template('home/choropleth_map.html')
    context = {'generatefilepath': passjspath,'inquery_date':inquery_date, 'sim_id': sim_id}
    return HttpResponse(template.render(context, request))


def csv_for_map_view(request, inquery_date, sim_id):
    allinfo = Data.objects.filter(date=inquery_date, simulation_id=sim_id)
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
    writer.writerow(['ID_ESPACIA','value'])
    for data_point in allinfo:
        if data_point.location.municipality_code in tricky_codes:
            data_point.location.municipality_code = data_point.location.municipality_code[1:]
            writer.writerow([data_point.location.municipality_code, data_point.value_mid])
        else:
            writer.writerow([data_point.location.municipality_code, data_point.value_mid])

    return HttpResponse(output.getvalue())


def display_simulations(request):
    simulationinfo = Simulation.objects.all()

    simulationlist = {}

    simulationlist2 = {'simulation_id': [], 'model_name': [], 'create_time': []}

    for entry in simulationinfo:
        simulationlist[entry.id] = entry.model_name
        simulationlist2['simulation_id'].append(str(entry.id))
        simulationlist2['model_name'].append(entry.model_name)
        simulationlist2['create_time'].append(entry.creation_timestamp)

    tests = ["simulation_id", "model_name", "create_time"]
    columns = [simulationlist2[test] for test in tests]
    max_len = len(max(columns, key=len))
    for col in columns:
        col +=[None,]*(max_len-len(col))

    rows = [[col[i] for col in columns] for i in range(max_len)]

    #print rows

    template = loader.get_template('home/simulation.html')
    context = {'simulationlist': simulationlist, 'simulationlist2': rows, 'tests': tests, }
    return HttpResponse(template.render(context, request))