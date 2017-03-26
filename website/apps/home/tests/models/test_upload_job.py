#!/bin/env python3
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
import datetime

import pytz
from django.contrib.auth.models import User
from django.test.testcases import TestCase

from website.apps.home.models import UploadJob


class UploadJobModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="user")

    def test_duration_new_1(self):
        upload_job = UploadJob.objects.create(
            name="Test",
            created_by=self.user,
            status=UploadJob.NEW,
            upload_start_timestamp=datetime.datetime(year=2016, month=1, day=1, tzinfo=pytz.UTC),
            upload_end_timestamp=datetime.datetime(year=2017, month=1, day=1, tzinfo=pytz.UTC)
        )
        self.assertEqual(upload_job.duration, None)

    def test_duration_new_2(self):
        upload_job = UploadJob.objects.create(
            name="Test",
            created_by=self.user,
            status=UploadJob.NEW,
        )
        self.assertEqual(upload_job.duration, None)

    def test_duration_in_progress_1(self):
        upload_job = UploadJob.objects.create(
            name="Test",
            created_by=self.user,
            status=UploadJob.IN_PROGRESS,
        )

        self.assertEqual(upload_job.duration, None)

    def test_duration_in_progress_2(self):
        upload_job = UploadJob.objects.create(
            name="Test",
            created_by=self.user,
            status=UploadJob.IN_PROGRESS,
            upload_start_timestamp=datetime.datetime(year=2016, month=1, day=1, tzinfo=pytz.UTC),
            upload_end_timestamp=None
        )
        upload_job.refresh_from_db()
        self.assertTrue(upload_job.duration > datetime.timedelta(450, 50575, 246971))

    def test_duration_in_progress_3(self):
        upload_job = UploadJob.objects.create(
            name="Test",
            created_by=self.user,
            status=UploadJob.IN_PROGRESS,
            upload_start_timestamp=datetime.datetime(year=2016, month=1, day=1, tzinfo=pytz.UTC),
            upload_end_timestamp=datetime.datetime(year=2017, month=1, day=1, tzinfo=pytz.UTC)
        )
        upload_job.refresh_from_db()
        self.assertTrue(upload_job.duration > datetime.timedelta(450, 50575, 246971))

    def test_duration_complete_1(self):
        upload_job = UploadJob.objects.create(
            name="Test",
            created_by=self.user,
            status=UploadJob.COMPLETED,
        )

        self.assertEqual(upload_job.duration, None)

    def test_duration_complete_2(self):
        upload_job = UploadJob.objects.create(
            name="Test",
            created_by=self.user,
            status=UploadJob.COMPLETED,
            upload_start_timestamp=datetime.datetime(year=2016, month=1, day=1, tzinfo=pytz.UTC),
            upload_end_timestamp=None
        )
        upload_job.refresh_from_db()
        self.assertEqual(upload_job.duration, None)

    def test_duration_complete_3(self):
        upload_job = UploadJob.objects.create(
            name="Test",
            created_by=self.user,
            status=UploadJob.COMPLETED,
            upload_start_timestamp=None,
            upload_end_timestamp=datetime.datetime(year=2016, month=1, day=1, tzinfo=pytz.UTC),
        )
        upload_job.refresh_from_db()
        self.assertEqual(upload_job.duration, None)

    def test_duration_complete_4(self):
        upload_job = UploadJob.objects.create(
            name="Test",
            created_by=self.user,
            status=UploadJob.COMPLETED,
            upload_start_timestamp=datetime.datetime(year=2016, month=1, day=1, tzinfo=pytz.UTC),
            upload_end_timestamp=datetime.datetime(year=2016, month=1, day=2, tzinfo=pytz.UTC),
        )
        upload_job.refresh_from_db()
        self.assertEqual(upload_job.duration, datetime.timedelta(1, 0, 0))

    def test_duration_failed_1(self):
        upload_job = UploadJob.objects.create(
            name="Test",
            created_by=self.user,
            status=UploadJob.FAILED,
            upload_start_timestamp=datetime.datetime(year=2016, month=1, day=1, tzinfo=pytz.UTC),
        )

        self.assertEqual(upload_job.duration, None)

    def test_duration_failed_2(self):
        upload_job = UploadJob.objects.create(
            name="Test",
            created_by=self.user,
            status=UploadJob.COMPLETED,
            upload_start_timestamp=datetime.datetime(year=2016, month=1, day=1, tzinfo=pytz.UTC),
            upload_end_timestamp=datetime.datetime(year=2016, month=1, day=2, tzinfo=pytz.UTC),
        )
        upload_job.refresh_from_db()
        self.assertEqual(upload_job.duration, datetime.timedelta(1, 0, 0))
