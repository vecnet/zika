#!/bin/env python3.4
# -*- coding: utf-8 -*-
#
# This file is part of the VecNet Zika modeling interface.
# For copyright and licensing information about this package, see the
# NOTICE.txt and LICENSE.txt files in its top-level directory; they are
# available at https://github.com/vecnet/zika
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License (MPL), version 2.0.  If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.test.testcases import TestCase
from django.test.utils import override_settings
from django.urls.base import reverse


class GoogleAnalyticsCodeTest(TestCase):
    def setUp(self):
        self.client.login(username="admin", password="1")

    @override_settings(DISABLE_GOOGLE_ANALYTICS=False,)
    def test_get_index(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("UA-90339757-1", str(response.content))

    @override_settings(DISABLE_GOOGLE_ANALYTICS=True)
    def test_database_get_none(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("UA-90339757-1", str(response.content))
        self.assertNotIn("https://www.google-analytics.com/analytics.js", str(response.content))
