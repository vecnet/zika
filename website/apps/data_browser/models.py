from __future__ import unicode_literals

from django.db import models


# Create your models here.
class ZikaCasesColumbia(models.Model):
    report_date = models.DateField()
    location = models.TextField()
    data_type = models.TextField()
    data_field_code = models.TextField()
    value = models.IntegerField()

    class Meta:
        db_table = "zika_cases"