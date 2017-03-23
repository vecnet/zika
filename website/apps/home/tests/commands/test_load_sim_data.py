# Copyright (C) 2016, University of Notre Dame
# All rights reserved
import io
import os
from django.core.files.base import File
from django.core.management import call_command
from django.test.testcases import TestCase

from website.apps.home.models import Simulation

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class LoadSimDataTest(TestCase):
    def setUp(self):
        data_file = File(io.StringIO(''))
        self.simulation = Simulation(
            name="test", historical=False, is_uploaded=False
        )
        self.simulation.data_file.save("test.csv", data_file, save=True)
        self.simulation.save()

    def test_success_empty_file(self):
        data_file = File(io.StringIO(''))
        simulation = Simulation(
            name="test", historical=False, is_uploaded=False
        )
        simulation.data_file.save("test.csv", data_file, save=True)
        simulation.save()

        call_command("load_sim_data", simulation.id)
        simulation.refresh_from_db()
        self.assertEqual(simulation.is_uploaded, True)
        self.assertEqual(simulation.data.count(), 0)
        self.assertEqual(simulation.totals_data.count(), 0)

    def test_success_one_liner(self):
        fp = open(os.path.join(BASE_DIR, 'data', 'upload1.csv'))
        self.simulation.data_file.save('test1.csv', fp, save=True)
        self.simulation.save()
        fp.close()

        call_command("load_sim_data", self.simulation.id)
        self.simulation.refresh_from_db()
        self.assertEqual(self.simulation.is_uploaded, True)
        self.assertEqual(self.simulation.data.count(), 1)
        data = self.simulation.data.all()[0]
        self.assertEqual(data.value_low, 1.0)
        self.assertEqual(data.value_mid, 2.0)
        self.assertEqual(data.value_high, 3.0)

        self.assertEqual(self.simulation.totals_data.count(), 1)
        totals_data = self.simulation.totals_data.all()[0]
        self.assertEqual(totals_data.total_low, 1.0)
        self.assertEqual(totals_data.total_mid, 2.0)
        self.assertEqual(totals_data.total_high, 3.0)
