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

from django.views.generic.list import ListView

from website.apps.home.models import Simulation


class ListModelView(ListView):
    """ List of simulations. Using the same template for historical and simulated data """
    template_name = "home/list_view.html"

    def get_queryset(self):
        if self.kwargs.get("is_historical", False):
            return Simulation.objects.filter(historical=True).order_by("-creation_timestamp")
        return Simulation.objects.filter(historical=False).order_by("-creation_timestamp")
