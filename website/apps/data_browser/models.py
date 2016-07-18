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


class MunicipalityCodes(models.Model):
    NOM_DEPART = models.TextField()
    COD_DEPTO = models.IntegerField()
    NOM_MUNICI = models.TextField()
    ID_ESPACIA = models.IntegerField()
    class Meta:
        db_table = "municipality_codes"

