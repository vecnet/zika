# Copyright (C) 2016, University of Notre Dame
# All rights reserved


# Copyright (C) 2016, University of Notre Dame
# All rights reserved
from django.test.testcases import TestCase
from django.test.utils import override_settings
from django.urls.base import reverse


class GoogleAnalyticsCodeTest(TestCase):
    def setUp(self):
        self.client.login(username="admin", password="1")

    @override_settings(DISABLE_GOOGLE_ANALYTICS=False,)
    def test_get_index(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("UA-90339757-1", str(response.content))

    @override_settings(DISABLE_GOOGLE_ANALYTICS=True)
    def test_database_get_none(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("UA-90339757-1", str(response.content))
        self.assertNotIn("https://www.google-analytics.com/analytics.js", str(response.content))
