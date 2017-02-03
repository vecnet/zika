# FUNCTIONS TO TEST
from django.test import TestCase

from website.apps.home.models import Totals
from website.apps.home.views.ChartView import format_totals_by_date, format_historical_totals


class Utils(TestCase):
    # import fixtures
    fixtures = ['test-fixtures/test-fixture-locations.json',
                'test-fixtures/test-fixture-simulations.json',
                'test-fixtures/test-fixture-simulation-model.json',
                'test-fixtures/test-fixture-totals.json']


    # Test aggregating data points returns expected values
    def test_format_totals_by_date(self):
        sim_id = 2
        sim_data = Totals.objects.filter(simulation_id=sim_id)

        data_dict = format_totals_by_date(sim_data)

        self.assertEqual(data_dict['mid_totals'], [[1438819200000.0, 2979.09252602774]])
        self.assertEqual(data_dict['range_totals'], [[1438819200000.0, 286.772913324014, 7102.14114399089]])

    # Test that aggregating historical data points returns expected values
    def test_sum_historical_data(self):
        sim_id = 1
        sim_data = Totals.objects.filter(simulation_id=sim_id, simulation__is_historical=True)

        data = format_historical_totals(sim_data)

        self.assertEqual(data, [[1438819200000.0, 2979.09252602774]])
