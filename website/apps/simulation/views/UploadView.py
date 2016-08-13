#!/bin/env python2
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

from django.http.response import HttpResponseBadRequest, HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.db import transaction

import logging

from website.apps.simulation.models import Simulation
from website.apps.simulation.utils import load_simulation_file

logger = logging.getLogger(__name__)

class UploadView(TemplateView):
    template_name = "simulation/upload.html"

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        uploaded_file = self.request.FILES.get(u"output_file", None)
        if not uploaded_file:
            return HttpResponseBadRequest("Not file[] file is provided")
        simulation_name = self.request.POST.get(u"name", None)
        logger.info("Filename: %s" % uploaded_file.name)

        load_simulation_file(uploaded_file.file, simulation_name=simulation_name)

        return HttpResponseRedirect("")