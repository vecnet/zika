# Copyright (C) 2016, University of Notre Dame
# All rights reserved
from django.db import models


class Location(models.Model):
    report_date = models.DateField(default='1999-01-01')
    location = models.TextField(default='')
    department = models.TextField(default='')
    municipality = models.TextField(default='')
    data_type = models.TextField(default='')
    data_field_code = models.TextField(default='')
    value = models.IntegerField(default=0)