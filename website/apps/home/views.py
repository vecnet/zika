# Copyright (C) 2016, University of Notre Dame
# All rights reserved
from django.views.generic.base import TemplateView
from django.http.response import HttpResponse

import csv


class IndexView(TemplateView):
    template_name = "home/index.html"


def load_locations(request, department_name):
    fp = open("municipality_codes.csv")
    csvpath = "https://raw.githubusercontent.com/cdcepi/zika/master/Colombia/Municipality_Zika/data/Municipality_Zika_2016-07-16.csv"
    codereader = csv.reader(open(csvpath), delimiter=',', quotechar='"')
    x = 1
    for row in codereader:
        if row[0] != 'report_date':
            x += 1

    print x
    return HttpResponse(content = x)
