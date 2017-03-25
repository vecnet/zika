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
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.test.testcases import TestCase

from website.apps.home.models import UploadJob, Simulation, Data, SimulationModel, Totals
from website.apps.home.utils import load_simulation_file


class LoadSimulationFileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user')

    def test_success(self):
        upload_job = UploadJob(
            name='Test',
            created_by=self.user,
        )
        data_file = ContentFile('''"id","model_name","population","disease","name","output_generate_date","value_low","value_mid","value_high","date","department","department_code","municipality","municipality_code"
"51639f09-929a-4b06-8371-59a7e40e93f5","data_cases_combo","all","ZVD","forecasted cases",2016-02-09 19:00:00,17.475,27,38,2016-02-09 19:00:00,"ANTIOQUIA","05","MEDELLN","05001"
        ''')
        upload_job.data_file.save('data.csv', data_file)
        upload_job = UploadJob.objects.get(id=upload_job.id)
        result, message = load_simulation_file(upload_job)
        self.assertEqual(result, True)
        self.assertEqual(Simulation.objects.count(), 1)
        self.assertEqual(Data.objects.count(), 1)
        simulation = Simulation.objects.all().first()
        data = Data.objects.all().first()
        self.assertEqual(simulation.is_uploaded, True)
        self.assertEqual(simulation.name, 'Test 2016-02-09')
        self.assertEqual(simulation.date_output_generated, datetime.date(2016, 2, 9))
        self.assertEqual(data.simulation, simulation)
        self.assertEqual(data.location.department, 'ANTIOQUIA')
        self.assertEqual(data.location.department_code, '05')
        self.assertEqual(data.location.municipality, 'MEDELLN')
        self.assertEqual(data.location.municipality_code, '05001')
        self.assertEqual(data.value_low, 17.475)
        self.assertEqual(data.value_mid, 27)
        self.assertEqual(data.value_high, 38)

    def test_success_totals(self):
        upload_job = UploadJob(
            name='Test',
            created_by=self.user,
        )
        data_file = ContentFile('''"id","model_name","population","disease","name","output_generate_date","value_low","value_mid","value_high","date","department","department_code","municipality","municipality_code"
"51639f09-929a-4b06-8371-59a7e40e93f5","data_cases_combo","all","ZVD","forecasted cases",2016-02-09 19:00:00,17.475,27,38,2016-02-09 19:00:00,"ANTIOQUIA","05","MEDELLN","05001"
"2ee3b9f2-de72-43d0-ac3f-a21b8c3d4a25","data_cases_combo","all","ZVD","forecasted cases",2016-02-09 19:00:00,20.475,29,39.525,2016-02-09 19:00:00,"ANTIOQUIA ","05"," MEDELLN","05001"
        ''')
        upload_job.data_file.save('data.csv', data_file)
        upload_job = UploadJob.objects.get(id=upload_job.id)
        result, message = load_simulation_file(upload_job)
        self.assertEqual(result, True)
        self.assertEqual(Simulation.objects.count(), 1)
        self.assertEqual(Data.objects.count(), 2)

        self.assertEqual(Totals.objects.count(), 1)
        simulation = Simulation.objects.all().first()
        totals = Totals.objects.all().first()
        self.assertEqual(simulation.is_uploaded, True)
        self.assertEqual(simulation.name, 'Test 2016-02-09')
        self.assertEqual(simulation.date_output_generated, datetime.date(2016, 2, 9))
        self.assertEqual(totals.simulation, simulation)
        self.assertEqual(totals.data_date, datetime.date(2016, 2, 9))
        self.assertEqual(totals.total_low, 37.95)
        self.assertEqual(totals.total_mid, 56)
        self.assertEqual(totals.total_high, 77.525)

    def test_success_multiple_simulations(self):
        upload_job = UploadJob(
            name="Test",
            created_by=self.user,
        )
        data_file = ContentFile('''"id","model_name","population","disease","name","output_generate_date","value_low","value_mid","value_high","date","department","department_code","municipality","municipality_code"
"51639f09-929a-4b06-8371-59a7e40e93f5","data_cases_combo","all","ZVD","forecasted cases",2016-02-09 19:00:00,17.475,27,38,2016-02-09 19:00:00,"ANTIOQUIA","05","MEDELLN","05001"
"2ee3b9f2-de72-43d0-ac3f-a21b8c3d4a25","data_cases_combo","all","ZVD","forecasted cases",2016-02-16 19:00:00,20.475,29,39.525,2016-02-16 19:00:00,"ANTIOQUIA ","05"," MEDELLN","05001"
        ''')
        upload_job.data_file.save('data.csv', data_file)
        result, message = load_simulation_file(upload_job)
        self.assertEqual(result, True)
        self.assertEqual(Simulation.objects.count(), 2)
        self.assertEqual(Data.objects.count(), 2)
        simulation1 = Simulation.objects.get(date_output_generated='2016-02-09')
        self.assertEqual(simulation1.is_uploaded, True)
        self.assertEqual(simulation1.name, 'Test 2016-02-09')
        self.assertEqual(simulation1.date_output_generated, datetime.date(2016, 2, 9))
        data1 = Data.objects.get(simulation=simulation1)
        self.assertEqual(data1.location.department, 'ANTIOQUIA')
        self.assertEqual(data1.location.department_code, '05')
        self.assertEqual(data1.location.municipality, 'MEDELLN')
        self.assertEqual(data1.location.municipality_code, '05001')
        self.assertEqual(data1.value_low, 17.475)
        self.assertEqual(data1.value_mid, 27)
        self.assertEqual(data1.value_high, 38)

        simulation2 = Simulation.objects.get(date_output_generated='2016-02-16')
        self.assertEqual(simulation2.is_uploaded, True)
        self.assertEqual(simulation2.name, 'Test 2016-02-16')
        data2 = Data.objects.get(simulation=simulation2)
        self.assertEqual(data2.location.department, 'ANTIOQUIA')
        self.assertEqual(data2.location.department_code, '05')
        self.assertEqual(data2.location.municipality, 'MEDELLN')
        self.assertEqual(data2.location.municipality_code, '05001')
        self.assertEqual(data2.value_low, 20.475)
        self.assertEqual(data2.value_mid, 29)
        self.assertEqual(data2.value_high, 39.525)

    def test_broken_csv(self):
        upload_job = UploadJob(
            name='Test',
            created_by=self.user,
        )
        data_file = ContentFile('''"id","population","disease","name","output_generate_date","value_low","value_mid","value_high","date","department","department_code","municipality","municipality_code"
"51639f09-929a-4b06-8371-59a7e40e93f5","all","ZVD","forecasted cases",2016-02-09 19:00:00,17.475,27,38,2016-02-09 19:00:00,"ANTIOQUIA","05","MEDELLN","05001"
        ''')
        upload_job.data_file.save('data.csv', data_file)
        upload_job = UploadJob.objects.get(id=upload_job.id)
        result, message = load_simulation_file(upload_job)
        self.assertEqual(result, False)
        self.assertEqual(message, 'KeyError: \'model_name\'')
        upload_job.refresh_from_db()
        self.assertEqual(upload_job.status, UploadJob.FAILED)
        self.assertEqual(upload_job.last_error_message, 'KeyError: \'model_name\'')
        self.assertEqual(Simulation.objects.count(), 0)
        self.assertEqual(Data.objects.count(), 0)

    def test_simulation_uploaded_already(self):
        upload_job = UploadJob(
            name='Test',
            created_by=self.user,
        )
        simulation = Simulation.objects.create(
            date_output_generated="2016-02-09",
            sim_model=SimulationModel.objects.create(model_name='data_cases_combo'),
            is_uploaded=True,
        )
        data_file = ContentFile('''"id","model_name","population","disease","name","output_generate_date","value_low","value_mid","value_high","date","department","department_code","municipality","municipality_code"
    "51639f09-929a-4b06-8371-59a7e40e93f5","data_cases_combo","all","ZVD","forecasted cases",2016-02-09 19:00:00,17.475,27,38,2016-02-09 19:00:00,"ANTIOQUIA","05","MEDELLN","05001"
    "2ee3b9f2-de72-43d0-ac3f-a21b8c3d4a25","data_cases_combo","all","ZVD","forecasted cases",2016-02-16 19:00:00,20.475,29,39.525,2016-02-16 19:00:00,"ANTIOQUIA ","05"," MEDELLN","05001"
            ''')
        upload_job.data_file.save('data.csv', data_file)
        result, message = load_simulation_file(upload_job)
        self.assertEqual(result, False)
        self.assertEqual(message, 'Simulation %s has been uploaded already. Can\'t update.' % simulation.id)
        upload_job.refresh_from_db()
        self.assertEqual(upload_job.status, UploadJob.FAILED)
        self.assertEqual(
            upload_job.last_error_message,
            'Simulation %s has been uploaded already. Can\'t update.' % simulation.id
        )

