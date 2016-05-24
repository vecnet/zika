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


import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


class LoginRequiredMixin(object):
    """ This works: class InterviewListView(LoginRequiredMixin, ListView)
    This DOES NOT work: class InterviewListView(ListView, LoginRequiredMixin)
    I'm not 100% sure that wrapping as_view function using Mixin is a good idea though, but whatever
    """
    @classmethod
    def as_view(cls, **initkwargs):
        # Ignore PyCharm warning below, this is a Mixin class after all
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)
