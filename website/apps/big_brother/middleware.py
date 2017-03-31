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

from django.db.transaction import atomic
from website.apps.big_brother.models import PageVisit
import logging

logger = logging.getLogger(__name__)

class BigBrotherMiddleware:
    def process_request(self, request, *args, **kwargs):
        user = request.user
        host =request.META.get("HTTP_HOST", "")
        querystring = None
        ip = request.META.get("REMOTE_ADDR", "")
        action = request.method
        user_agent = request.META.get("HTTP_USER_AGENT", "")
        http_referrer = request.META.get("HTTP_REFERER", "")

        if not user.is_authenticated():
            user = None

        # Save up to 4096 bytes of request body in the database
        post_content = str(request.body[:4096])
        # b'123\xfd' -> 123\xfd
        post_content = post_content[2:-1]

        try:
            with atomic():
                # "with atomic" if required to abort failed transaction
                # If DataError occurs (i.e. post_content = "\xff\xff\xff\xff"), than transaction is in the
                # bad state, it not possible to execute new queries in that transaction
                # django.db.transaction.TransactionManagementError is raised
                #
                # This all try/atomic/except thing can now be removed as the bug with saving binary data to
                # database has been resolved, and create function doesn't fail anymore
                page_visit = PageVisit.objects.create(
                    user=user,
                    url=request.path,
                    host=host,
                    ip=ip,
                    action=action,
                    user_agent=user_agent,
                    http_referrer=http_referrer,
                    post_content=post_content
                )
                request.page_visit = page_visit
        except Exception as e:
            logger.critical("Big Brother - can't save PageVisit: %s" % e)

    def process_response(self, request, response):
        if hasattr(request, "page_visit"):
            request.page_visit.http_code = response.status_code
            try:
                request.page_visit.save()
            except Exception as e:
                logger.critical("Big Brother - can't save PageVisit in process_response: %s" % e)

        return response
