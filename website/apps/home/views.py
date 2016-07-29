# Copyright (C) 2016, University of Notre Dame
# All rights reserved
from django.views.generic.base import TemplateView


class IndexView(TemplateView):
    template_name = "home\index.html"


class Locations(TemplateView):
    template_name = "home\locations.html"


def load_locations(request):
    fp = open("municipality_codes.csv")