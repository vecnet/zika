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

from django.contrib.auth.models import User
from django.test.client import Client
from django.test.testcases import TestCase
from django.urls.base import reverse

from website.apps.home.models import Simulation


class DeleteSimulationViewTest(TestCase):
    def setUp(self):
        admin = User.objects.create(username="admin")
        admin.set_password("1")
        admin.is_superuser = True
        admin.is_staff = True
        admin.save()
        self.simulation = Simulation.objects.create()
        self.url = reverse("simulation.delete", kwargs={"simulation_id": self.simulation.id})
        self.client.login(username="admin", password="1")

    def test_anonymous(self):
        client = Client()
        response = client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_non_admin(self):
        user = User.objects.create(username="user")
        user.set_password("1")
        user.save()
        client = Client()
        client.login(username="user", password="1")
        self.assertEqual(Simulation.objects.all().count(), 1)
        response = client.get(self.url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Simulation.objects.all().count(), 1)

    def test_success(self):
        self.assertEqual(Simulation.objects.all().count(), 1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("home.list_view"))
        self.assertEqual(Simulation.objects.all().count(), 0)
