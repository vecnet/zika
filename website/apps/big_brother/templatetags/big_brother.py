# Copyright (C) 2015, University of Notre Dame
# All rights reserved


from django import template
from ..models import PageVisit

register = template.Library()


@register.filter()
def last_visits(value, number=25):
    return PageVisit.objects.all().order_by("-timestamp")[:number]
