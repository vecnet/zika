#!/bin/env python3
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

from django.core.management.base import BaseCommand

from website.apps.home.models import UploadJob
from website.apps.home.utils import load_simulation_file

job = None

import signal
import sys
def signal_handler(signal, frame):
    global job
    job.status = UploadJob.FAILED
    job.last_error_message = 'SIGINT received, upload job terminated'
    job.save(update_fields=['status', 'last_error_message'])
    sys.exit(0)

class Command(BaseCommand):
    help = 'Upload csv data file and save objects in database'

    def add_arguments(self, parser):
        parser.add_argument('job_id', type=int)

    def handle(self, *args, **options):
        """
        Upload data file
        :param args:
        :param options:
        :return:
        """
        global job
        # Signal handler for SIGINT (set UploadJob status to "FAILED")
        # On Windows, signal() can only be called with SIGABRT, SIGFPE, SIGILL, SIGINT, SIGSEGV, or SIGTERM.
        # A ValueError will be raised in any other case.
        signal.signal(signal.SIGINT, signal_handler)
        job_id = options['job_id']
        job = UploadJob.objects.get(id=job_id)
        print('Starting data upload, job_id %s' % job_id)
        result, message = load_simulation_file(job)
        if result:
            print('Successfully loaded data')
        else:
            print('Error: %s' % message)
