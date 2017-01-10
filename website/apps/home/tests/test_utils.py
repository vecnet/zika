# FUNCTIONS TO TEST
import io

from django.test import TestCase

from website.apps.home.models import Simulation, Data
from website.apps.home.utils import load_simulation_file
from website.apps.home.views.ChartView import sum_cases_by_date


class Utils(TestCase):
    # import fixtures
    fixtures = ['test-fixtures/test-fixture-locations.json',
                'test-fixtures/test-fixture-simulations.json',
                'test-fixtures/test-fixture-simulation-model.json',
                'test-fixtures/test-fixture-data-sample-with-historical.json']

    # Test that load simulation file passes with both parameters
    def test_load_simulation_file_pass(self):
        myfile = "test-file-upload-DO-NOT-DELETE.csv"
        simulation_name = 'test simulation'
        historical = False

        load_simulation_file(myfile, simulation_name, historical)

        simulation = Simulation.objects.filter(name=simulation_name)

        self.assertEqual(simulation.count(), 1)
        self.assertEqual(simulation[0].name, 'test simulation')
        self.assertEqual(simulation[0].historical, False)

    # Test if simulation name is None
    def test_load_simulation_file_fail_none_sim_name(self):
        myfile = io.StringIO('name,output_generate_date,value_mid,value_high,disease,model_name,'
                             'department,municipality_code,municipality,department_code,date,value_low,'
                             'id,population')
        simulation_name = None

        self.assertRaises(TypeError, load_simulation_file, (myfile, simulation_name))

    # Test if no simulation name provided
    def test_load_simulation_file_fail_no_sim_name(self):
        myfile = io.StringIO('name,output_generate_date,value_mid,value_high,disease,model_name,'
                             'department,municipality_code,municipality,department_code,date,value_low,'
                             'id,population')

        self.assertRaises(TypeError, load_simulation_file, myfile)

    # Test if file is None
    def test_load_simulation_file_fail_none_file(self):
        myfile = None
        simulation_name = "test 4"

        self.assertRaises(TypeError, load_simulation_file, (myfile, simulation_name))

    # Test if no file provided
    def test_load_simulation_file_fail_no_file(self):
        simulation_name = "test 4"

        self.assertRaises(TypeError, load_simulation_file, simulation_name)

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
