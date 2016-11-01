from django.test import TestCase, Client
from django.urls.base import reverse
from datetime import date


# FUNCTIONS TO TEST
class Home(TestCase):
    # import fixtures
    fixtures = ['test_simulation_data.json', 'test_location.json', 'test_simulation.json', 'test_location_data.json']

    def setUp(self):
        self.client = Client()

    def test_choropleth(self):
        inquery_date = date(2015, 8, 6)
        sim_id = 1

        url = reverse(
            "choropleth_map",
            kwargs={"inquery_date": inquery_date, "sim_id": sim_id}
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        # I don't know how to test that something is rendering a map

    def test_csv_for_map_view_pass(self):
        "csv for map test"
        inquery_date = date(2015, 8, 6)
        sim_id = 1

        url = reverse(
            "csv_for_map",
            kwargs={"inquery_date": inquery_date, "sim_id": sim_id}
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEquals('ID_ESPACIA,value\r\n5001,0.0\r\n5002,0.0\r\n5004,0.0\r\n5021,0.0\r\n', response.content)

    def test_csv_for_map_view_fail(self):
        "csv for map test"
        inquery_date = date(2013, 8, 6)
        sim_id = 1

        url = reverse(
            "csv_for_map",
            kwargs={"inquery_date": inquery_date, "sim_id": sim_id}
        )

        response = self.client.get(url)
        print response.content
        self.assertEqual(response.status_code, 200)
        # self.assertEquals('ID_ESPACIA,value\r\n5001,0.0\r\n5002,0.0\r\n5004,0.0\r\n5021,0.0\r\n', response.content)


    def test_display_simulations(self):

        url = reverse(
            "simulation.list"
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
