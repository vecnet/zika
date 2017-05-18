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
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.base import TemplateView

from website.apps.home.models import Simulation


class HomeView(TemplateView):
    template_name = "home/home.html"

    def get_context_data(self, **kwargs):
        # Get the most recent simulation so that clicking the Map View button will go to the appropriate page
        try:
            latest_simulation = Simulation.objects.exclude(historical=True).latest('creation_timestamp')
            sim_id = latest_simulation.id
            model_id = latest_simulation.sim_model.id
        except ObjectDoesNotExist:
            sim_id = None
            model_id = None
        context = {
            "most_recent_sim_id": sim_id,
            "most_recent_model_id": model_id,
        }

        return context
