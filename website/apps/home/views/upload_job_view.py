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

from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from website.apps.home.models import UploadJob
from website.apps.home.serializers import UploadJobSerializer


@csrf_exempt
def upload_job_view(request, pk):
    """
    Retrieve, update or delete an upload job
    """
    if not request.user.is_superuser:
        raise PermissionDenied
    try:
        upload_job = UploadJob.objects.get(pk=pk)
    except UploadJob.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = UploadJobSerializer(upload_job)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = UploadJobSerializer(upload_job, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        upload_job.delete()
        return HttpResponse(status=204)
