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

from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.management import call_command
from django.test.testcases import TestCase

from website.apps.home.models import UploadJob, Simulation, SimulationModel


class LoadDataTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user')
        self.upload_job = UploadJob(
            name='Test',
            created_by=self.user,
        )
        data_file = ContentFile('''"id","model_name","population","disease","name","output_generate_date","value_low","value_mid","value_high","date","department","department_code","municipality","municipality_code"
        "51639f09-929a-4b06-8371-59a7e40e93f5","data_cases_combo","all","ZVD","forecasted cases",2016-02-09 19:00:00,17.475,27,38,2016-02-09 19:00:00,"ANTIOQUIA","05","MEDELLN","05001"
                ''')
        self.upload_job.data_file.save('data.csv', data_file)

    def test_success(self):
        self.assertEqual(Simulation.objects.count(), 0)
        call_command("load_data", self.upload_job.id)
        self.upload_job.refresh_from_db()
        self.assertEqual(self.upload_job.status, UploadJob.COMPLETED)
        self.assertEqual(self.upload_job.last_error_message, "")
        self.assertEqual(Simulation.objects.count(), 1)

    def test_fail(self):
        simulation = Simulation.objects.create(
            date_output_generated="2016-02-09",
            sim_model=SimulationModel.objects.create(model_name='data_cases_combo'),
            is_uploaded=True,
        )
        self.assertEqual(Simulation.objects.count(), 1)
        call_command("load_data", self.upload_job.id)
        self.upload_job.refresh_from_db()
        self.assertEqual(self.upload_job.status, UploadJob.FAILED)
        self.assertEqual(
            self.upload_job.last_error_message,
            'Simulation %s has been uploaded already. Can\'t update.' % simulation.id
        )
        self.assertEqual(Simulation.objects.count(), 1)