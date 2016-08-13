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

from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from website.apps.simulation.models import Location
from website.apps.simulation.models import Simulation


# @method_decorator(login_required, name='dispatch')
class BrowseView(TemplateView):
    template_name = "simulation/browse.html"

    def get_context_data(self, **kwargs):
        context = {
            "locations": Location.objects.all(),
            "simulations": Simulation.objects.all(),
        }
        return context
