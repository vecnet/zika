#!/bin/env python2
# -*- coding: utf-8 -*-
#
# This file is part of the VecNet Zika modeling interface.
# For copyright and licensing information about this package, see the
# NOTICE.txt and LICENSE.txt files in its top-level directory; they are
# available at https://github.com/vecnet/zika
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License (MPL), version 2.0.  If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.


#
# class Location(models.Model):
#     report_date = models.DateField(default='1999-01-01')
#     location = models.TextField(default='')
#     department = models.TextField(default='')
#     municipality = models.TextField(default='')
#     data_type = models.TextField(default='')
#     data_field_code = models.TextField(default='')
#     value = models.IntegerField(default=0)

from django.contrib.auth.models import User
from django.db import models


class Location(models.Model):
    """
    Represents location in the database
    """
    department = models.TextField(blank=True)
    department_code = models.TextField(blank=True)
    municipality = models.TextField(blank=True)
    municipality_code = models.TextField(blank=True)
    creation_timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "location"
        verbose_name = "Location"
        verbose_name_plural = "Locations"
        # get_latest_by specifies the default field to use in your model Manager's latest() and earliest() methods.
        get_latest_by = "creation_timestamp"
        managed = True  # Django manages the database table's lifecycle.
        ordering = ["department", "municipality"]  # The default ordering for the object, for use when obtaining lists of objects:

    def __str__(self):
        return "%s - %s" % (self.municipality, self.department)


class SimulationModel(models.Model):
    """ Simulation Model """
    model_name = models.CharField(blank=False, max_length=100)
    creation_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s" % self.model_name


class Simulation(models.Model):
    name = models.TextField()
    # model_name = models.TextField(blank=True)
    sim_model = models.ForeignKey(SimulationModel, null=True, blank=True, related_name="simulation_model")
    disease = models.TextField(default="ZVD")
    date_output_generated = models.DateField(null=True, blank=True)
    creation_timestamp = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, null=True, related_name="simulations")
    data_file = models.FileField(upload_to="simulation_files")
    historical = models.BooleanField(default=False)

    class Meta:
        db_table = "simulation"
        verbose_name = "Simulation"
        verbose_name_plural = "Simulation"
        # get_latest_by specifies the default field to use in your model Manager's latest() and earliest() methods.
        get_latest_by = "creation_timestamp"
        managed = True  # Django manages the database table's lifecycle.
        ordering = ["date_output_generated"]  # The default ordering for the object, for use when obtaining lists of objects:

    def __str__(self):
        return "%s" % self.name

    def getfilename(self):
        return "%s" % self.data_file


class Data(models.Model):
    """ Simulation data """
    # ??? Do we even need that ???
    #  uuid - For compatibility with EpiJSON format
    uuid = models.TextField(blank=True)
    location = models.ForeignKey(Location)
    value_low = models.FloatField(null=False)
    value_mid = models.FloatField(null=True, blank=True)
    value_high = models.FloatField(null=True, blank=True)
    date = models.DateField(null=False)
    simulation = models.ForeignKey(Simulation, related_name="data")
    creation_timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "data"
        verbose_name = "Data"
        verbose_name_plural = "Data"
        # get_latest_by specifies the default field to use in your model Manager's latest() and earliest() methods.
        get_latest_by = "date"
        managed = True  # Django manages the database table's lifecycle.
        ordering = ["date"]  # The default ordering for the object, for use when obtaining lists of objects:

    def __str__(self):
        return "%s" % self.value_mid
