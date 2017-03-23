import io
from datetime import date

import time
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls.base import reverse

from website.apps.home.models import Simulation


class Home(TestCase):
    fixtures = ['test-fixtures/test-fixture-sim1-aug6-data_shortened.json',
                'test-fixtures/test-fixture-locations.json',
                'test-fixtures/test-fixture-simulations.json',
                'test-fixtures/test-fixture-simulation-model.json',
                'test-fixtures/test-fixture-totals.json']

    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create(username="admin", is_superuser=True, is_staff=True)
        self.admin.set_password("1")
        self.admin.save()

    def test_mapview_pass(self):
        model_id = 2
        sim_id = 2

        url = reverse(
            "home.mapview",
            kwargs={"model_id": model_id, "sim_id": sim_id}
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['current_sim'].id, 2)
        # self.assertEqual(response.context['generatefilepath'], '/home/csv_for_map/2/2015-08-06/')
        self.assertEqual(response.context['iframe_src'], '/home/chart/2/total/')

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
        self.assertEqual(response.context['current_sim'].id, 2)
        # self.assertEqual(response.context['generatefilepath'], '/home/csv_for_map/2/2015-08-06/')
        self.assertEqual(response.context['iframe_src'], '/home/chart/2/99524/')

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

    def test_display_historical(self):

        url = reverse(
            "home.display_historical"
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['historical_list'][0]['simulation_name'], 'historical data cases combo')
        self.assertEqual(response.context['historical_list'][0]['simulation_id'], '1')

    def test_country_total_chart_view(self):
        sim_id = 2

        url = reverse(
            "home.countrytotalchart",
            kwargs={"simulation_id": sim_id}
        )

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['simulation'].id, 2)
        self.assertEqual(response.context['simulation_mids'], [[1440028800000.0, 3135.96808488268],
                                                               [1440633600000.0, 3177.3048931069],
                                                               [1441238400000.0, 3155.27605852072]])
        self.assertEqual(response.context['simulation_range'], [[1440028800000.0, 276.106981186517, 7001.27887646723],
                                                                [1440633600000.0, 283.597569014026, 7028.99098585279],
                                                                [1441238400000.0, 299.543765159763, 7129.35462907125]])
        self.assertEqual(response.context['sim_generated_date_ms'], 1464825600000.0)

    def test_chart_view(self):
        sim_id = 2
        municipality_code = 99524

        url = reverse(
            "simulation.chart",
            kwargs={"simulation_id": sim_id, "municipality_code": municipality_code}
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['simulation'].id, 2)
        self.assertEqual(response.context['location'].department_code, '99')
        self.assertEqual(response.context['location'].department, "VICHADA")
        self.assertEqual(response.context['location'].municipality_code, '99524')
        self.assertEqual(response.context['location'].municipality, "LA PRIMAVERA")
        self.assertEqual(response.context['sim_generated_date_ms'], 1464825600000.0)

    def test_upload_view_get_anonymous(self):
        response = self.client.post(reverse('simulation.upload'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_upload_view_post_anonymous(self):
        response = self.client.post(reverse('simulation.upload'), data={})
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_upload_view_get_not_superuser(self):
        user = User.objects.create(username='user')
        user.set_password('1')
        user.save()
        self.client.login(username='user', password='1')
        response = self.client.get(reverse('simulation.upload'))
        self.assertEqual(response.status_code, 403)

    def test_upload_view_post_not_superuser(self):
        user = User.objects.create(username='user')
        user.set_password('1')
        user.save()
        self.client.login(username='user', password='1')
        response = self.client.post(reverse('simulation.upload'), data={})
        self.assertEqual(response.status_code, 403)

    def test_upload_view_get_success(self):
        self.client.login(username='admin', password='1')
        response = self.client.get(reverse('simulation.upload'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('simulationNameInput', str(response.content))

    def test_upload_view_post_no_output_file(self):
        self.client.login(username='admin', password='1')
        response = self.client.post(reverse('simulation.upload'), data={'name': 'test'})
        # Missing parameter: "'output_file'"
        self.assertEqual(response.status_code, 400)
        self.assertIn("Missing parameter", str(response.content))
        self.assertIn("output_file", str(response.content))

    def test_upload_view_post_no_name(self):
        self.client.login(username='admin', password='1')
        response = self.client.post(reverse('simulation.upload'), data={'output_file': io.StringIO("")})
        # Missing parameter: "'name'"
        self.assertEqual(response.status_code, 400)
        self.assertIn("Missing parameter", str(response.content))
        self.assertIn("name", str(response.content))

    def test_upload_view_post_no_historical(self):
        self.client.login(username='admin', password='1')
        response = self.client.post(
            reverse('simulation.upload'),
            data={'name': 'test', 'output_file': io.StringIO("")}
        )
        # Missing parameter: "'name'"
        self.assertEqual(response.status_code, 400)
        self.assertIn("Missing parameter", str(response.content))
        self.assertIn("historical", str(response.content))

    def test_upload_view_post_success_historical(self):
        simulation_count = Simulation.objects.count()
        self.client.login(username='admin', password='1')
        response = self.client.post(
            reverse('simulation.upload'),
            data={'name': 'test', 'output_file': io.StringIO(''), 'historical': 'on', 'is_test': 'yes'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('home.display_historical'))
        time.sleep(0.1)
        self.assertEqual(Simulation.objects.count(), simulation_count + 1)
        simulation = Simulation.objects.get(name='test')
        self.assertEqual(simulation.historical, True)
        self.assertEqual(simulation.is_uploaded, False)
        # Note due to "transactional" nature of Django unit tests, it is impossible to test
        # data loading code here

    def test_upload_view_post_success_not_historical(self):
        simulation_count = Simulation.objects.count()
        self.client.login(username='admin', password='1')
        response = self.client.post(
            reverse('simulation.upload'),
            data={'name': 'test', 'output_file': io.StringIO(''), 'historical': 'no', 'is_test': 'yes'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('home.display_simulations'))
        time.sleep(0.1)
        self.assertEqual(Simulation.objects.count(), simulation_count + 1)
        simulation = Simulation.objects.get(name='test')
        self.assertEqual(simulation.historical, False)
        self.assertEqual(simulation.is_uploaded, False)
        # Note due to "transactional" nature of Django unit tests, it is impossible to test
        # data loading code here
