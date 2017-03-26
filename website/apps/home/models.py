#!/bin/env python3.4
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

from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now


class Location(models.Model):
    """
    Represents location in the database
    """
    department = models.TextField(blank=True)
    department_code = models.TextField(blank=True, db_index=True)
    municipality = models.TextField(blank=True)
    municipality_code = models.TextField(blank=True, db_index=True)
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
    sim_model = models.ForeignKey(SimulationModel, null=True, blank=True, related_name="simulation_model")
    disease = models.TextField(default="ZVD")
    date_output_generated = models.DateField(null=True, blank=True)
    creation_timestamp = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, null=True, related_name="simulations")
    data_file = models.FileField(upload_to="simulation_files")
    historical = models.BooleanField(default=False)
    is_uploaded = models.BooleanField(default=False)

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
    date = models.DateField(null=False, db_index=True)
    simulation = models.ForeignKey(Simulation, related_name="data", db_index=True)
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


class Totals(models.Model):
    """ Totals for estimates by date """
    data_date = models.DateField(null=False, db_index=True)
    total_low = models.FloatField(null=False)
    total_mid = models.FloatField(null=True, blank=True)
    total_high = models.FloatField(null=True, blank=True)
    simulation = models.ForeignKey(Simulation, related_name="totals_data")
    date_output_generated = models.DateField(null=True, blank=True, db_index=True)

    def __str__(self):
        return "Sim ID: %s Date: %s, mid: %s  range: [ %s, %s]" % (self.simulation.id, self.data_date, self.total_mid,
                                                                   self.total_low, self.total_high)


class UploadJob(models.Model):
    """ Upload Job holds information for file upload process running in background
    """
    NEW = "New"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    FAILED = "Failed"

    name = models.TextField(default=None)
    status = models.TextField(default=NEW)
    last_error_message = models.TextField(blank=True, default="")
    data_file = models.FileField(null=True, blank=True, upload_to='simulation_files')
    historical = models.BooleanField(default=False)
    progress = models.IntegerField(blank=True, default=0) # Upload progress 0 to 100
    created_by = models.ForeignKey(User)
    creation_timestamp = models.DateTimeField(auto_now=True)
    # When upload process started
    upload_start_timestamp = models.DateTimeField(null=True, blank=True)
    upload_end_timestamp = models.DateTimeField(null=True, blank=True)
    pid = models.TextField(blank=True)  # Process ID of the process uploading data
    simulations = models.ManyToManyField(Simulation, related_name='upload_jobs')
    stdout_file = models.FileField(null=True, blank=True, upload_to='output')
    stderr_file = models.FileField(null=True, blank=True, upload_to='output')

    def __str__(self):
        return "%s (%s)" % (self.name, self.status)

    @property
    def duration(self):
        if self.status in (self.COMPLETED, self.FAILED):
            try:
                return self.upload_end_timestamp - self.upload_start_timestamp
            except TypeError:
                # TypeError: unsupported operand type(s) for -: 'NoneType' and 'NoneType'
                # TypeError: unsupported operand type(s) for -: 'datetime.datetime' and 'NoneType'
                # TypeError: unsupported operand type(s) for -: 'NoneType' and 'datetime.datetime'
                return None
        if self.status == self.IN_PROGRESS:
            try:
                return now() - self.upload_start_timestamp
            except TypeError:
                # TypeError: unsupported operand type(s) for -: 'datetime.datetime' and 'NoneType'
                return None
        return None


    class Meta:
        db_table = "upload_job"
        verbose_name = "Upload Job"
        verbose_name_plural = "Upload Jobs"
        managed = True  # Django manages the database table's lifecycle.
