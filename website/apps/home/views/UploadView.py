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
import logging

from subprocess import Popen

from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseBadRequest, HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.conf import settings
from website.apps.home.models import Simulation


logger = logging.getLogger(__name__)


class UploadView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "home/upload.html"

    def test_func(self):
        if not self.request.user.is_superuser:
            raise PermissionDenied
        else:
            return True

    def post(self, request):
        try:
            data_file = request.FILES['output_file']
            sim_name = request.POST['name']
            is_historical = request.POST['historical']
            is_test = request.POST.get('is_test', None)
        except KeyError as e:
            return HttpResponseBadRequest("Missing parameter: %s" % e)

        if is_historical == "on":
            is_historical = True
        else:
            is_historical = False

        # Create the simulation and save it
        simulation = Simulation.objects.create(
            name=sim_name, data_file=data_file, historical=is_historical, is_uploaded=False
        )

        if not is_test:
            # Skip executing load_sim_data command if executing from Django test client
            # because all unit tests are executed inside of a transaction and load_sim_data command won't see
            # simulation we just created and will fail

            # Capture output from the management command for debugging purpose
            outfile = open('logs/load_sim_data_stdout', 'w')
            errfile = open('logs/load_sim_data_stderr', 'w')
            p = Popen(
                [settings.PYTHON_EXECUTABLE, 'manage.py', 'load_sim_data', str(simulation.id)],
                stdout=outfile, stderr=errfile
            )
            logger.debug("PID %s started for loading simulation data in background" % p.pid)

        # Redirect to appropriate page whether uploading simulation or historical
        if is_historical != True:
            return HttpResponseRedirect(reverse('home.display_simulations'))
        else:
            return HttpResponseRedirect(reverse('home.display_historical'))
