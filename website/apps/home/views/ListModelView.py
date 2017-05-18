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
    context_object_name = 'simulations'

    def get_queryset(self):
        queryset = super(ListModelView, self).get_queryset()
        queryset = queryset.filter(historical=False).order_by("-creation_timestamp")
        if self.request.GET.get('filter'):
            queryset = queryset.filter(sim_model=self.request.GET.get('filter'), historical=False).order_by("-creation_timestamp")
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ListModelView, self).get_context_data(**kwargs)
        # Get a list of all the models in the system
        model_list_queryset = SimulationModel.objects.all()

        # Get the historical and simulated objects
        historical_simulation_list = Simulation.objects.filter(historical=True).order_by("-creation_timestamp")

        # Get the most recent simulation for the map view link
        latest_simulation = Simulation.objects.exclude(historical=True).latest('creation_timestamp')

        context["model_list"] = model_list_queryset
        context["historical_simulation_list"] = historical_simulation_list
        context["model_filter"] = self.request.GET.get('filter')
        context["most_recent_model_id"] = latest_simulation.sim_model.id
        context["most_recent_sim_id"] = latest_simulation.id

        return context
