from django.http.response import HttpResponse
from django.shortcuts import render


# Create your views here.
from website.apps.data_browser.models import ZikaCasesColumbia


def hello(request):

    new_case = ZikaCasesColumbia.objects.create(
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

    return HttpResponse(content="hello")