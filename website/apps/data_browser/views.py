from django.http.response import HttpResponse
from django.shortcuts import render
from django.template import loader

from website.apps.data_browser.models import ZikaCasesColumbia
from website.apps.data_browser.models import MunicipalityCodes
import csv
import json
# Create your views here.


# test function
def hello(request, hello_id):

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

    csvpath = "/Users/bingyushen/Downloads/municipality_codes.csv"
    codereader = csv.reader(open(csvpath), delimiter=',', quotechar='"')

    for row in codereader:
        if row[0]!='NOM_DEPART':
            mcode = MunicipalityCodes()
            mcode.NOM_DEPART = row[0]
            mcode.COD_DEPTO = row[1]
            mcode.NOM_MUNICI = row[2]
            mcode.ID_ESPACIA = row[3]
            mcode.save()'''
    return HttpResponse(content=hello_id)


# get all the locations from database
def location_list(request):
    locationlist = ZikaCasesColumbia.objects.filter(data_field_code='CO0003', report_date='2016-01-09')
    template = loader.get_template('data_browser/locationlist.html')
    context = {'all_locations': locationlist, }
    return HttpResponse(template.render(context, request))


# get info of location from database
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


# put detail info of specific location into highchart
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


# test function of put info of locations in EpiJSON file into highchart
def testchart(request, chartID='chartID', chart_type='line', chart_height=500):
    #load json data into python dictionary
    with open('/Users/bingyushen/Documents/zika/zika/pycharmz/website/apps/data_browser/jsonfiles/valid_test.json') as json_data:
        testdata = json.load(json_data)

    #define a local python dictionary to extract dates and value
    dataseries = [
        {'dates': [], 'value': []},
        {'dates': [], 'value': []},
        {'dates': [], 'value': []},
        {'dates': [], 'value': []},
    ]

    #defina a local python dictionary to extract location name
    locationinfo = [
        {'locationname': (), 'municipality_code': ()},
        {'locationname': (), 'municipality_code': ()},
        {'locationname': (), 'municipality_code': ()},
        {'locationname': (), 'municipality_code': ()},
    ]

    locationname = []
    #municipality_code = []

    #extract dates, value and location name into particular dictionaries
    for item in dataseries:
        y = dataseries.index(item)
        locationname1 = testdata["records"][y]["attributes"][1]["value"]
        locationname2 = testdata["records"][y]["attributes"][3]["value"]
        locationinfo[y]['locationname'] = str(locationname1+"_"+locationname2)
        locationname.append(locationname1+"_"+locationname2)
        #municipality_code.append(testdata["records"][y]["attributes"][4]["value"])
        locationinfo[y]['municipality_code'] = str(testdata["records"][y]["attributes"][4]["value"])
        for x in range(0, 3):
            item['dates'].append(str(testdata["records"][y]["events"][x]["date"]))
            item['value'].append(testdata["records"][y]["events"][x]["attributes"][1]["value"])

    #chart information and passing data to plot
    chartinfo = "working with data in EpiJSON format"
    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
    title = {"text": 'Data of 4 locations, 3 prediction dates'}
    xAxis = {"title": {"text": 'Dates'}, "categories": dataseries[0]['dates']}
    yAxis = {"title": {"text": 'Cases'}}

    series = [
    {"name": str(locationname[0]), "data": dataseries[0]['value']},
    {"name": str(locationname[1]), "data": dataseries[1]['value']},
    {"name": str(locationname[2]), "data": dataseries[2]['value']},
    {"name": str(locationname[3]), "data": dataseries[3]['value']},
    ]

    return render(request, 'data_browser/chart.html', {'chartID': chartID, 'chart': chart, 'series': series,
                                                       'title': title, 'xAxis': xAxis, 'yAxis': yAxis,
                                                       'print_locations': chartinfo, 'locationname': locationname,
                                                       'municipality_code': locationinfo
                                                       },)


# get info of location from EpiJSON file and put into highchart
def getlocationinfo(request, municipality_code, chartID='chartID', chart_type='line', chart_height=500):
    # load json data into python dictionary
    with open(
            '/Users/bingyushen/Documents/zika/zika/pycharmz/website/apps/data_browser/jsonfiles/valid_test.json') as json_data:
        testdata = json.load(json_data)

    # define a local python dictionary to extract dates and value
    dataseries = [
        {'dates': [], 'value': []},
        {'dates': [], 'value': []},
        {'dates': [], 'value': []},
    ]

    # extract dates, value and location name into particular dictionaries
    for x in range(0,4):
        print municipality_code
        print testdata["records"][x]["attributes"][4]["value"]
        print "====="
        if str(municipality_code) == str(testdata["records"][x]["attributes"][4]["value"]):
            print "hello"
            for y in range(0,3):
                for z in range(0,3):
                    dataseries[z]['dates'].append(str(testdata["records"][x]["events"][y]["date"]))
                    dataseries[z]['value'].append(testdata["records"][x]["events"][y]["attributes"][z]["value"])


    # chart information and passing data to plot
    chartinfo = "working with data in EpiJSON format"
    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
    title = {"text": 'Data of 4 locations, 3 prediction dates'}
    xAxis = {"title": {"text": 'Dates'}, "categories": dataseries[0]['dates']}
    yAxis = {"title": {"text": 'Cases'}}

    series = [
        {"name": 'low', "data": dataseries[0]['value']},
        {"name": 'mid', "data": dataseries[1]['value']},
        {"name": 'high', "data": dataseries[2]['value']},
    ]
    print dataseries
    return render(request, 'data_browser/detail.html', {'chartID': chartID, 'chart': chart, 'series': series,
                                                       'title': title, 'xAxis': xAxis, 'yAxis': yAxis,
                                                       'print_locations': chartinfo, })

