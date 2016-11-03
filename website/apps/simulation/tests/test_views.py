from django.test import TestCase, Client
from django.urls.base import reverse
from datetime import date
import StringIO

# FUNCTIONS TO TEST
class Simulation(TestCase):
    # import fixtures
    fixtures = ['simulation_data.json']

    def setUp(self):
        self.client = Client()

    def test_browse_view(self):
        url = reverse(
            "simulation.browse"
        )
        response = self.client.get(url)
        print response.context['simulations']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['locations']), 1122)
        self.assertEqual(response.context['simulations'].count(), 1)
        self.assertEqual(response.context['simulations'][0].name, '')
        self.assertEqual(response.context['simulations'][0].model_name, 'data_cases_combo')

    def test_chart_view(self):
        url = reverse(
            "simulation.chart",
            kwargs={"simulation_id": 1, "municipality_code": '05001'}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['data']), 44)
        self.assertEqual(str(response.context['location'].department), 'ANTIOQUIA')
        self.assertEqual(str(response.context['location'].municipality), 'MEDELLN')
        self.assertEqual(response.context['simulation'].name, '')
        self.assertEqual(response.context['simulation'].model_name, 'data_cases_combo')

    def test_upload_view(self):
        url = reverse(
            "simulation.upload",
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)


    def test_upload_view_post(self):
        url = reverse(
            "simulation.upload",
        )
        response = self.client.post(url, data={'name': 'test', 'output_file': StringIO.StringIO("put_generate_date,value_mid,value_high,disease,model_name,department,municipality_code,municipality,department_code,date,value_low,id,population")})

        self.assertEqual(response.status_code, 302)
