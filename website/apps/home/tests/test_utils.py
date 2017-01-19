# FUNCTIONS TO TEST
from django.test import TestCase

from website.apps.home.models import Data
from website.apps.home.views.ChartView import sum_cases_by_date


class Utils(TestCase):
    # import fixtures
    fixtures = ['test-fixtures/test-fixture-locations.json',
                'test-fixtures/test-fixture-simulations.json',
                'test-fixtures/test-fixture-simulation-model.json',
                'test-fixtures/test-fixture-data-sample-with-historical.json']


    # Test aggregating data points returns expected values
    def test_sum_cases_by_date(self):
        sim_id = 2
        sim_data = Data.objects.filter(simulation_id=sim_id)

        data_dict = sum_cases_by_date(sim_id, sim_data)

        self.assertEqual(data_dict['mid_totals'], [[1438819200000.0, 7.149786503589542]])
        self.assertEqual(data_dict['range_totals'], [[1438819200000.0, 0.8077659017070163, 27.17384548025155]])

    # Test that aggregating historical data points returns expected values
    def test_sum_historical_data(self):
        sim_id = 1
        sim_data = Data.objects.filter(simulation_id=sim_id)

        data_dict = sum_cases_by_date(sim_id, sim_data)

        self.assertEqual(data_dict['mid_totals'], [[1438819200000.0, 4.0]])
        self.assertEqual(data_dict['range_totals'], [[1438819200000.0, 4.0, 10.37387371211298]])
