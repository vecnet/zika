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
    return HttpResponseRedirect(reverse("home.list_view"))
