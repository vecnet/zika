from django.http.response import HttpResponse
from django.shortcuts import render
import csv
import sys, os
from website.apps.data_browser.models import ZikaCasesColumbia
from django.template import loader

# Create your views here.

# csvfilepath = "/Users/bingyushen/Downloads/zika-master/Colombia/Municipality_Zika/data"

def hello(request):

    '''new_case = ZikaCasesColumbia.objects.create(
        report_date="1990-01-01",
        location="Chicago",
        data_field_code="CODE",
        data_type="case",
        value=1,
    )

    ZikaCasesColumbia.objects.delete()
    for case in ZikaCasesColumbia.objects.all():
        if case.report_date is None:
            case.report_date = "2006-04-05"
        case.value = case.value + 1
        case.save()
        print "id: %s" % case.pk
        print "report_date: %s" % case.report_date
        print "location: " + case.location
        print "value: %s " % case.value

    # import data in csv files into database
    for name in os.listdir(csvfilepath):
        csvfilename = csvfilepath+"/"+name
        datareader = csv.reader(open(csvfilename), delimiter=',')

        for row in datareader:
            if row[0] != 'report_date':
                zikacase = ZikaCasesColumbia()
                zikacase.report_date = row[0]
                zikacase.location = row[1]
                zikacase.data_type = row[3]
                zikacase.data_field_code = row[4]
                zikacase.value = row[7]
                zikacase.save()'''

    # static table display


    return HttpResponse(content="hello")


def stable(request):
    value_list_across_time = ZikaCasesColumbia.objects.filter(data_field_code='CO0002', location='Colombia-Antioquia-Caucasia')
    template = loader.get_template('data_browser/data_browser.html')
    context = {'query_results': value_list_across_time,}
    return HttpResponse(template.render(context, request))