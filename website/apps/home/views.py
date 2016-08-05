# Copyright (C) 2016, University of Notre Dame
# All rights reserved
from django.views.generic.base import TemplateView
from django.http.response import HttpResponse
from django.shortcuts import render

import csv
import io
from urllib2 import urlopen


class IndexView(TemplateView):
    template_name = "home/index.html"


def testview(request):
    print "test"
    return HttpResponse(content="hello")


def load_locations(request, department_name, chartID='chartID', chart_type='line', chart_height=500):
    chart_department =  department_name
    department_name = department_name[:-11]
    print department_name

    allfile = [
            "Municipality_Zika_2016-01-09.csv", "Municipality_Zika_2016-01-16.csv",
            "Municipality_Zika_2016-01-23.csv", "Municipality_Zika_2016-01-30.csv",
            "Municipality_Zika_2016-02-06.csv", "Municipality_Zika_2016-02-13.csv",
            "Municipality_Zika_2016-02-20.csv", "Municipality_Zika_2016-02-27.csv",
            "Municipality_Zika_2016-03-05.csv", "Municipality_Zika_2016-03-12.csv",
            "Municipality_Zika_2016-03-19.csv", "Municipality_Zika_2016-03-26.csv",
            "Municipality_Zika_2016-04-02.csv", "Municipality_Zika_2016-04-09.csv",
            "Municipality_Zika_2016-04-16.csv", "Municipality_Zika_2016-04-23.csv",
            "Municipality_Zika_2016-04-30.csv", "Municipality_Zika_2016-05-07.csv",
            "Municipality_Zika_2016-05-14.csv", "Municipality_Zika_2016-05-21.csv",
            "Municipality_Zika_2016-05-28.csv", "Municipality_Zika_2016-06-04.csv",
            "Municipality_Zika_2016-06-11.csv", "Municipality_Zika_2016-06-18.csv",
            "Municipality_Zika_2016-06-25.csv", "Municipality_Zika_2016-07-02.csv",
            "Municipality_Zika_2016-07-09.csv", "Municipality_Zika_2016-07-16.csv"
            ]
    filename = []
    dateseries = []

    for item in allfile:
        csvpath = "https://raw.githubusercontent.com/cdcepi/zika/master/Colombia/Municipality_Zika/data/"+item
        filename.append(csvpath)
        dateseries.append(item[18:-4])
    count1 = []
    count2 = []
    count3 = []
    count4 = []
    #csvpath = "https://raw.githubusercontent.com/cdcepi/zika/master/Colombia/Municipality_Zika/data/Municipality_Zika_2016-07-16.csv"
    #csvpath = "https://github.com/cdcepi/zika/blob/master/Colombia/Municipality_Zika/data/Municipality_Zika_2016-01-09.csv"
    for item in filename:
        webpage = urlopen(item)
        codereader = csv.reader(webpage)
        w = 0
        x = 0
        y = 0
        z = 0
        for row in codereader:
            if row[0] != 'report_date':
                if row[1].decode('utf-8').find(department_name) == -1:
                    continue
                else:
                    if row[4].decode('utf-8').find("CO0001") == 0:
                        w += int(row[7])
                    elif row[4].decode('utf-8').find("CO0002") == 0:
                        x += int(row[7])
                    elif row[4].decode('utf-8').find("CO0003") == 0:
                        y += int(row[7])
                    #elif row[4].decode('utf-8').find("CO0004") == 0:
                        #z += int(row[7])
        count1.append(w)
        count2.append(x)
        count3.append(y)
        #count4.append(z)

    chart_title = "data from online csv"

    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
    title = {"text": str(chart_title)}
    xAxis = {"title": {"text": 'Dates'}, "categories": dateseries}
    yAxis = {"title": {"text": 'Cases'}}

    series = [
        {"name": 'zika_confirmed_laboratory', "data": count1},
        #{"name": 'zika_confirmed_clinic', "data": count2},
        {"name": 'zika_suspected', "data": count3},
        #{"name": 'zika_suspected_clinic', "data": count4},
    ]

    return render(request, 'home/departmentchart.html', {'chartID': chartID, 'chart': chart, 'series': series,
                                                        'title': title, 'xAxis': xAxis, 'yAxis': yAxis,
                                                        'chart_title': chart_title, 'department_name': chart_department})


