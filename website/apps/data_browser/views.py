from django.http.response import HttpResponse
from django.shortcuts import render
from django.template import loader

from website.apps.data_browser.models import ZikaCasesColumbia
from website.apps.data_browser.models import MunicipalityCodes
import csv
import json
# Create your views here.


def hello(request, helloid):

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
        print "value: %s " % case.value'''

    csvpath = "/Users/bingyushen/Downloads/municipality_codes.csv"
    codereader = csv.reader(open(csvpath), delimiter=',', quotechar='"')

    for row in codereader:
        if row[0]!='NOM_DEPART':
            mcode = MunicipalityCodes()
            mcode.NOM_DEPART = row[0]
            mcode.COD_DEPTO = row[1]
            mcode.NOM_MUNICI = row[2]
            mcode.ID_ESPACIA = row[3]
            mcode.save()
    return HttpResponse(content="hello")


def location_list(request):
    locationlist = ZikaCasesColumbia.objects.filter(data_field_code='CO0003', report_date='2016-01-09')
    template = loader.get_template('data_browser/locationlist.html')
    context = {'all_locations': locationlist, }
    return HttpResponse(template.render(context, request))


def location_info(request, query_location):
    value_list_across_time_c1 = ZikaCasesColumbia.objects.filter(data_field_code='CO0001',
                                            location=query_location)
    value_list_across_time_c2 = ZikaCasesColumbia.objects.filter(data_field_code='CO0002',
                                            location=query_location)
    value_list_across_time_c3 = ZikaCasesColumbia.objects.filter(data_field_code='CO0003',
                                            location=query_location)

    tabledata = {'dates': [], 'valuec1': [], 'valuec2': [], 'valuec3': []}

    for case in value_list_across_time_c1:
        tabledata['dates'].append(case.report_date.strftime('%y/%m/%d'))
        tabledata['valuec1'].append(case.value)

    for case in value_list_across_time_c2:
        tabledata['valuec2'].append(case.value)

    for case in value_list_across_time_c3:
        tabledata['valuec3'].append(case.value)

    template = loader.get_template('data_browser/locationinfo.html')
    context = {'query_results_c1': value_list_across_time_c1,
               'query_results_c2': value_list_across_time_c2,
               'query_results_c3': value_list_across_time_c3,
               'tabledata': tabledata,
               'location_url': query_location, }
    return HttpResponse(template.render(context, request))


def location_info_chart(request, chart_location, chartID='chart_ID', chart_type='line', chart_height=500):
    value_list_across_time_c1 = ZikaCasesColumbia.objects.filter(data_field_code='CO0001',
                                                                 location=chart_location)
    value_list_across_time_c2 = ZikaCasesColumbia.objects.filter(data_field_code='CO0002',
                                                                 location=chart_location)
    value_list_across_time_c3 = ZikaCasesColumbia.objects.filter(data_field_code='CO0003',
                                                                 location=chart_location)
    hcdata_c1 = {'dates': [], 'value': [], }
    hcdata_c2 = {'dates': [], 'value': [], }
    hcdata_c3 = {'dates': [], 'value': [], }

    for case in value_list_across_time_c1:
        hcdata_c1['dates'].append(case.report_date.strftime('%y/%m/%d'))
        hcdata_c1['value'].append(case.value)

    for case in value_list_across_time_c2:
        hcdata_c2['dates'].append(case.report_date.strftime('%y/%m/%d'))
        hcdata_c2['value'].append(case.value)

    for case in value_list_across_time_c3:
        hcdata_c3['dates'].append(case.report_date.strftime('%y/%m/%d'))
        hcdata_c3['value'].append(case.value)

    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height, }
    title = {"text": 'Data with data_field_code CO0001, CO0002, CO0003'}
    xAxis = {"title": {"text": 'Dates'}, "categories": hcdata_c1['dates']}
    yAxis = {"title": {"text": 'Cases'}}
    series = [
        {"name": 'CO0001_Cases', "data": hcdata_c1['value']},
        {"name": 'CO0002_Cases', "data": hcdata_c2['value']},
        {"name": 'CO0003_Cases', "data": hcdata_c3['value']},
    ]
    return render(request, 'data_browser/chart.html', {'chartID': chartID, 'chart': chart, 'series': series,
                                                       'title': title, 'xAxis': xAxis, 'yAxis': yAxis,
                                                       'print_locations': chart_location})


def testchart(request, chartID='chart_ID', chart_type='line', chart_height=500):
    #json_data = open('/Users/bingyushen/Documents/zika/zika/pycharmz/website/apps/data_browser/jsonfiles/valid_test.json')
    #metadata = json_data['metadata']
    #records = json_data['records']
    #modelname = data['metadata'][0]['model_name']
    #return HttpResponse(modelname)

    with open('/Users/bingyushen/Documents/zika/zika/pycharmz/website/apps/data_browser/jsonfiles/valid_test.json') as json_data:
        testdata = json.load(json_data)
    #print testdata["metadata"]
    #print "===="
    #print testdata["records"][0]["events"][1]["attributes"][0]["value"]

    dataseries1 = {'dates': [], 'value': [], }
    dataseries2 = {'dates': [], 'value': [], }
    dataseries3 = {'dates': [], 'value': [], }
    dataseries4 = {'dates': [], 'value': [], }

    for x in range(0, 3):
        dataseries1['dates'].append(testdata["records"][0]["events"][x]["date"])
        dataseries1['value'].append(testdata["records"][0]["events"][x]["attributes"][1]["value"])

    for x in range(0, 3):
        dataseries2['dates'].append(testdata["records"][1]["events"][x]["date"])
        dataseries2['value'].append(testdata["records"][1]["events"][x]["attributes"][1]["value"])

    for x in range(0, 3):
        dataseries3['dates'].append(testdata["records"][2]["events"][x]["date"])
        dataseries3['value'].append(testdata["records"][2]["events"][x]["attributes"][1]["value"])

    for x in range(0, 3):
        dataseries4['dates'].append(testdata["records"][3]["events"][x]["date"])
        dataseries4['value'].append(testdata["records"][3]["events"][x]["attributes"][1]["value"])

    locationname11 = testdata["records"][0]["attributes"][1]["value"]
    locationname12 = testdata["records"][0]["attributes"][3]["value"]

    locationname21 = testdata["records"][1]["attributes"][1]["value"]
    locationname22 = testdata["records"][1]["attributes"][3]["value"]

    locationname31 = testdata["records"][2]["attributes"][1]["value"]
    locationname32 = testdata["records"][2]["attributes"][3]["value"]

    locationname41 = testdata["records"][3]["attributes"][1]["value"]
    locationname42 = testdata["records"][3]["attributes"][3]["value"]

    location1 = locationname11 + locationname12
    location2 = locationname21 + locationname22
    location3 = locationname31 + locationname32
    location4 = locationname41 + locationname42

    chartinfo = "working with data in EpiJson format"
    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
    title = {"text": 'info of 4 locations, 3 prediction dates'}
    xAxis = {"title": {"text": 'Dates'}, "categories": ['2016-08-16T00:00:00Z', '2016-08-23T00:00:00Z', '2016-08-30T00:00:00Z']}
    yAxis = {"title": {"text": 'Cases'}}
    series = [
        {"name": 'location1', "data": dataseries1['value']},
        {"name": 'location2', "data": dataseries2['value']},
        {"name": 'location3', "data": dataseries3['value']},
        {"name": 'location4', "data": dataseries4['value']},
    ]
    return render(request, 'data_browser/chart.html', {'chartID': chartID, 'chart': chart, 'series': series,
                                                       'title': title, 'xAxis': xAxis, 'yAxis': yAxis,
                                                       'print_locations': chartinfo})
