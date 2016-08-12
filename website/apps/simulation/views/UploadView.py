# Copyright (C) 2016, University of Notre Dame
# All rights reserved
from django.http.response import HttpResponseBadRequest, HttpResponseRedirect
from django.views.generic.base import TemplateView

import logging

from website.apps.simulation.models import Simulation

logger = logging.getLogger(__name__)

class UploadView(TemplateView):
    template_name = "simulation/upload.html"

    def post(self, request, *args, **kwargs):
        uploaded_file = self.request.FILES.get(u"output_file", None)
        if not uploaded_file:
            return HttpResponseBadRequest("Not file[] file is provided")
        simulation_name = self.request.POST.get(u"name", None)
        logger.info("Filename: %s" % uploaded_file.name)

        simulation = Simulation.objects.create(name=simulation_name)

        return HttpResponseRedirect("")