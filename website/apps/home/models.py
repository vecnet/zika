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

from django.db import models


class Location(models.Model):
    report_date = models.DateField(default='1999-01-01')
    location = models.TextField(default='')
    department = models.TextField(default='')
    municipality = models.TextField(default='')
    data_type = models.TextField(default='')
    data_field_code = models.TextField(default='')
    value = models.IntegerField(default=0)

