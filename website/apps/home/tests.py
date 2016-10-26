from django.test import TestCase, Client
from django.urls.base import reverse
from datetime import date


# FUNCTIONS TO TEST
class Home(TestCase):
    # import fixtures
    fixtures = ['test_simulation_data.json', 'test_location.json', 'test_simulation.json']

    def setUp(self):
        self.client = Client()

    def test_csv_for_map_view(self):
        # Create a client for testing with
        # client = Client()

        inquery_date = date(2015, 8, 6)
        sim_id = 1

        url = reverse(
            "csv_for_map",
            kwargs={"inquery_date": inquery_date, "sim_id": sim_id}
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEquals('ID_ESPACIA,value\r\n5001,0.0\r\n5002,0.0\r\n5004,0.0\r\n5021,0.0\r\n', response.content)


    def test_csv_for_map_view(self):
        # Create a client for testing with
        # client = Client()

        inquery_date = date(2015, 8, 6)
        sim_id = 1

        url = reverse(
            "csv_for_map",
            kwargs={"inquery_date": inquery_date, "sim_id": sim_id}
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEquals('ID_ESPACIA,value\r\n5001,0.0\r\n5002,0.0\r\n5004,0.0\r\n5021,0.0\r\n', response.content)
