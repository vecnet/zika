# Copyright (C) 2016, University of Notre Dame
# All rights reserved
from django.views.generic.base import TemplateView
from django.http.response import HttpResponse
from django.shortcuts import render

import csv
import io
from urllib2 import urlopen

from website.apps.home.models import Location

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
    chart_department =  department_name
    department_name = department_name[:-11]
    print department_name

    dateseries = []
    dateseries1 = {'dates':[], }
    datac1 = Location.objects.filter(data_field_code='CO0001', department=department_name)
    countc1 = []
    countc2 = []
    countc3 = []
    countc4 = []

    for item in datac1:
        if item.report_date not in dateseries:
            dateseries.append(item.report_date)
    print dateseries

    for item in dateseries:
        datac1 = Location.objects.filter(report_date=item, department=department_name, data_field_code='CO0001')
        datac2 = Location.objects.filter(report_date=item, department=department_name, data_field_code='CO0002')
        datac3 = Location.objects.filter(report_date=item, department=department_name, data_field_code='CO0003')
        datac4 = Location.objects.filter(report_date=item, department=department_name, data_field_code='CO0004')
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

    chart_title = "data from local database"

    chart = {"renderTo": chartID, "type": 'spline', "height": 500}
    title = {"text": str(chart_title)}
    xAxis = {"title": {"text": 'Dates'}, "categories": dateseries1['dates']}
    yAxis = {"title": {"text": 'Cases'}}

    series = [
        {"name": 'zika_confirmed_laboratory', "data": countc1},#"dashStyle": 'longdash', "color": '#FF0000'
        #{"name": 'zika_confirmed_clinic', "data": countc2},
        {"name": 'zika_suspected', "data": countc3, "zoneAxis": 'x', "zones": [{"value": 5}, {"dashStyle": 'dot'}]},
        #{"name": 'zika_suspected_clinic', "data": countc4},
    ]

    return render(request, 'home/departmentchart.html', {'chartID': chartID, 'chart': chart, 'series': series,
                                                        'title': title, 'xAxis': xAxis, 'yAxis': yAxis,
                                                        'chart_title': chart_title, 'department_name': chart_department})

def testmap(request):
    return render(request,'home/testmap.html')