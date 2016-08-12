# Copyright (C) 2016, University of Notre Dame
# All rights reserved
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