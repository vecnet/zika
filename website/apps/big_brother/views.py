# Copyright (C) 2016, University of Notre Dame
# All rights reserved
import logging
import os

from django.http.response import HttpResponse

from website.database_apps.big_brother.models import TrackingCode

logger = logging.getLogger(__name__)
static_dir = os.path.join(os.path.dirname((os.path.abspath(__file__))), "static", "big_brother")


def tracking_code_view(request, tracking_code, callback=None):
    """ This view is to track which invitation emails were read by users """
    with open(os.path.join(static_dir, "1x1.png"), "rb") as fp:
        png = fp.read()

    # Capture information about user
    # host = request.META.get("HTTP_HOST", "")
    ip = request.META.get("REMOTE_ADDR", "")
    action = request.method
    user_agent = request.META.get("HTTP_USER_AGENT", "")
    http_referrer = request.META.get("HTTP_REFERER", "")

    tracking_code_object = TrackingCode.objects.create(
        # url=request.path,
        # host=host,
        code=tracking_code,
        ip=ip,
        action=action,
        user_agent=user_agent,
        http_referrer=http_referrer,
    )

    if callback:
        callback(request, tracking_code, tracking_code_object)

    return HttpResponse(png, content_type="image/png")
