# Copyright (C) 2015, University of Notre Dame
# All rights reserved
from django.contrib.auth.models import User
from django.db import models


class PageVisit(models.Model):
    host = models.TextField()
    url = models.TextField()
    querystring = models.TextField()
    # GET, POST, etc
    action = models.TextField()
    http_code = models.TextField()
    http_referrer = models.TextField()
    user_agent = models.TextField()
    ip = models.TextField()
    # Auto saves on create
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True, blank=True)
    post_content = models.TextField(default="")

    def __unicode__(self):
        return "%s" % self.url


class TrackingCode(models.Model):
    code = models.TextField(blank=True)
    action = models.TextField(blank=True)
    http_referrer = models.TextField(blank=True)
    user_agent = models.TextField(blank=True)
    ip = models.TextField(blank=True)
    # Auto saves on create
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s" % self.code

    class Meta:
        get_latest_by = 'timestamp'
        managed = True  # Django manages the database table's lifecycle.
        ordering = ['timestamp', ]
