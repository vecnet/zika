from datetime import date

from django.test import TestCase, Client
from django.urls.base import reverse

from .utils.find_html_element_by_id import FindHTMLElementById


class Home(TestCase):
    fixtures = ['test-fixtures/test-fixture-sim1-aug6-data_shortened.json', 'test-fixtures/test-fixture-locations.json',
                'test-fixtures/test-fixture-simulation1.json', 'test-fixtures/test-fixture-simulationmodel.json']

    def setUp(self):
        self.client = Client()

    def test_mapview_pass(self):
        model_id = 2
        sim_id = 2

        url = reverse(
            "home.mapview",
            kwargs={"model_id": model_id, "sim_id": sim_id}
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        parser = FindHTMLElementById("iframe2")
        parser.feed(response.content.decode(encoding="latin-1"))
        self.assertTrue(parser.is_found)
        self.assertFalse(parser.is_duplicated_id)
        self.assertEqual(parser.tag, "iframe")

    def test_mapview_with_municipality_pass(self):
        model_id = 2
        sim_id = 2
        municipality_code = 99524

        url = reverse(
            "home.mapview",
            kwargs={"model_id": model_id, "sim_id": sim_id, "municipality_code": municipality_code}
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        parser = FindHTMLElementById("iframe2")
        parser.feed(response.content.decode(encoding="latin-1"))
        self.assertTrue(parser.is_found)
        self.assertFalse(parser.is_duplicated_id)
        self.assertEqual(parser.tag, "iframe")

    def test_csv_for_map_view_pass(self):
        inquery_date = date(2015, 8, 6)
        sim_id = 2

        url = reverse(
            "home.csv_for_map",
            kwargs={"inquery_date": inquery_date, "sim_id": sim_id}
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEquals(b'ID_ESPACIA,value\r\n5001,1.0\r\n5002,1.0\r\n5004,1.0\r\n5021,1.0\r\n', response.content)

    def test_csv_for_map_view_fail(self):
        inquery_date = date(2013, 8, 6)
        sim_id = 1

        url = reverse(
            "home.csv_for_map",
            kwargs={"inquery_date": inquery_date, "sim_id": sim_id}
        )

        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)

    def test_display_simulations(self):

        url = reverse(
            "home.display_simulations"
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['simulation_model_list'][0]['simulation_name'], 'test data 1')
        self.assertEqual(response.context['simulation_model_list'][0]['simulation_id'], '2')
