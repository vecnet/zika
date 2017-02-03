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
        self.assertEqual(data_dict['mid_totals'], [[1440028800000.0, 3135.96808488268],
                                                   [1440633600000.0, 3177.3048931069],
                                                   [1441238400000.0, 3155.27605852072]])
        self.assertEqual(data_dict['range_totals'], [[1440028800000.0, 276.106981186517, 7001.27887646723],
                                                     [1440633600000.0, 283.597569014026, 7028.99098585279],
                                                     [1441238400000.0, 299.543765159763, 7129.35462907125]])

    # Test that aggregating historical data points returns expected values
    def test_format_historical_totals(self):
        sim_id = 1
        sim_data = Totals.objects.filter(simulation_id=sim_id)

        data = format_historical_totals(sim_data)

        self.assertEqual(data, [[1439424000000.0, 2979.09252602774]])
