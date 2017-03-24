# Copyright (C) 2016, University of Notre Dame
# All rights reserved
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls.base import reverse

from website.apps.home.models import Simulation
from website.notification import set_notification, SUCCESS


@login_required
def delete_simulation_view(request, simulation_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    simulation = get_object_or_404(Simulation, pk=simulation_id)
    simulation.delete()
    set_notification(request, "Successfully deleted simulation", SUCCESS)
    return HttpResponseRedirect(reverse("home.display_simulations"))
