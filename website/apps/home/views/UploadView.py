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

from subprocess import Popen

from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseBadRequest, HttpResponseRedirect
from django.views.generic.base import TemplateView

from website.apps.home.models import Simulation


class UploadView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "../templates/simulation/upload.html"

    def test_func(self):
        if not self.request.user.is_superuser:
            raise PermissionDenied
        else:
            return True

    def post(self, request):
        if request.method == 'POST':
            if not request.FILES['output_file']:
                return HttpResponseBadRequest("No 'output_file' is provided")
            else:
                sim_name = self.request.POST.get(u"name", None)
                is_historical = self.request.POST.get("historical")

                if is_historical == "on":
                    is_historical = True
                else:
                    is_historical = False

                # Create the simulation and save it
                simulation = Simulation.objects.create(name=sim_name, data_file=request.FILES['output_file'],
                                                       historical=is_historical, is_uploaded=False)
                simulation.save()

                new_sim = Simulation.objects.get(id=simulation.id)
                if new_sim:

                    outfile = open('logs/outfile', 'w')
                    errfile = open('logs/errfile', 'w')

                    p = Popen(["/home/beth/.virtualenvs/vecnetzika-py3/bin/python3.4", "manage.py",
                                          "load_sim_data", str(new_sim.id)], stdout=outfile, stderr=errfile)

                # Redirect to appropriate page whether uploading simulation or historical
                if is_historical != True:
                    return HttpResponseRedirect(reverse('home.display_simulations'))
                else:
                    return HttpResponseRedirect(reverse('home.display_historical'))
        else:
            return HttpResponseRedirect("")
