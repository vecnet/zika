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

import logging

from django.core.urlresolvers import reverse
from django.db import transaction
from django.http.response import HttpResponseBadRequest, HttpResponseRedirect
from django.views.generic.base import TemplateView

from website.apps.home.utils import load_simulation_file

logger = logging.getLogger(__name__)


class UploadView(TemplateView):
    template_name = "../templates/simulation/upload.html"

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            if not request.FILES['output_file']:
                return HttpResponseBadRequest("No 'output_file' is provided")
            else:
                sim_name = self.request.POST.get(u"name", None)
                is_historical = self.request.POST.get("historical")
                load_simulation_file(request.FILES['output_file'], simulation_name=sim_name, is_historical=is_historical)

                # Redirect to appropriate page whether uploading simulation or historical
                if is_historical!='on':
                    return HttpResponseRedirect(reverse('home.display_simulations'))
                else:
                    return HttpResponseRedirect(reverse('home.display_historical'))
        else:
            return HttpResponseRedirect("")
