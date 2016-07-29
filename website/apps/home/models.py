# Copyright (C) 2016, University of Notre Dame
# All rights reserved
from django.db import models


class Location(models.Model):
    department = models.TextField()
    municipality = models.TextField()
