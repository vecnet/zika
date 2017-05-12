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

from website.apps.home.models import Simulation, SimulationModel


class ListModelView(ListView):
    """ List of simulations. Using the same template for historical and simulated data """
    template_name = "home/list_view.html"
    model = Simulation

    def get_context_data(self, **kwargs):
        # Get a list of all the models in the system
        model_list_queryset = SimulationModel.objects.filter()
        model_list = []
        for model in model_list_queryset:
            model_list.append(model)

        # Get the historical and simulated objects
        historical_simulation_list = Simulation.objects.filter(historical=True).order_by("-creation_timestamp")
        simulation_list = Simulation.objects.filter(historical=False).order_by("-creation_timestamp")

        context = {
            "model_list": model_list,
            "simulation_list": simulation_list,
            "historical_simulation_list": historical_simulation_list,
        }

        return context
