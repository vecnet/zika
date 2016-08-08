# Copyright (C) 2016, University of Notre Dame
# All rights reserved
from django.db import models


class Location(models.Model):
    report_date = models.DateField()
    location = models.TextField()
    department = models.TextField()
    municipality = models.TextField()
    data_type = models.TextField()
    data_field_code = models.TextField()
    value = models.IntegerField()