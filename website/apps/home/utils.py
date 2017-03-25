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

import csv
import logging

from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import now

from website.apps.home.models import Location, Data, Simulation, SimulationModel, Totals, UploadJob

logger = logging.getLogger(__name__)


def load_simulation_file(upload_job):
    """
    :param upload_job:
    :type upload_job: website.apps.home.models.UploadJob
    :return:
    """
    # csvfile = upload_job.data_file.file
    # dialect = csv.Sniffer().sniff(csvfile.read(1024))
    # csvfile.seek(0)
    # Reopen in binary mode
    # upload_job.data_file.close()
    upload_job.status = UploadJob.IN_PROGRESS
    upload_job.upload_start_timestamp = now()
    upload_job.save(update_fields=['status', 'upload_start_timestamp'])
    try:
        csvfile = upload_job.data_file
        # Workaround for Bug #13809
        # https://code.djangoproject.com/ticket/13809
        # It is fixed in Django 1.11, so it will be possible to use upload_job.data_file.open("r")
        # But we are on Django 1.10 yet
        csvfile = upload_job.data_file.storage.open(upload_job.data_file.name, "r")
        in_memory_csv = []
        for row in csvfile:
            in_memory_csv.append(row)

        dictreader = csv.DictReader(in_memory_csv)

        line = None
        simulation_set = set()
        lines_read = 0

        for line in dictreader:
            lines_read += 1
            if lines_read % 100 == 0:
                upload_job.progress = int(100 * float(lines_read) / len(in_memory_csv))
                upload_job.save(update_fields=['progress'])
            if line['output_generate_date'] is None:
                # Assuming this is an empty line
                continue
            # Assuming date is in "YYYY-MM-DD HH:MM:SS" format
            # However, YYYY-MM-DD works, too
            date_output_generated = line['output_generate_date'].split(" ")[0]
            # Get or Create the SimulationModel object
            sim_model = SimulationModel.objects.get_or_create(model_name=line['model_name'].strip())[0]
            sim = Simulation.objects.filter(date_output_generated=date_output_generated, sim_model=sim_model).first()
            if sim and sim.is_uploaded:
                msg = 'Simulation %s has been uploaded already. Can\'t update.' % sim.id
                logger.error(msg)
                upload_job.status = UploadJob.FAILED
                upload_job.last_error_message = msg
                upload_job.save(update_fields=['status', 'last_error_message'])
                return False, msg
            if not sim:
                sim = Simulation(
                    name='%s %s' % (upload_job.name, str(date_output_generated)),
                    sim_model=sim_model,
                    date_output_generated=date_output_generated,
                    historical=upload_job.historical,
                    is_uploaded=False,
                    created_by=upload_job.created_by,
                )

            location = Location.objects.filter(
                department_code=line['department_code'].strip(),
                municipality_code=line['municipality_code'].strip(),
            ).first()

            if not location:
                location = Location.objects.create(
                    department=line['department'].strip(),
                    department_code=line['department_code'].strip(),
                    municipality=line['municipality'].strip(),
                    municipality_code=line['municipality_code'].strip(),
                )

            if location.department != line['department']:
                print("WARNING: department name mismatch (%s, %s)" % (location.department, line['department']))

            if location.municipality != line['municipality']:
                print("WARNING: municipality name mismatch (%s, %s)" % (location.municipality, line['municipality']))
            sim.save()
            simulation_set.add(sim)

            Data.objects.create(
                location=location,
                date=line['date'].split(" ")[0],  # Assuming date is in "YYYY-MM-DD HH:MM:SS" format
                simulation=sim,
                value_low=line['value_low'].strip(),
                value_mid=line['value_mid'].strip(),
                value_high=line['value_high'].strip(),
            )

            try:
                total_obj = Totals.objects.get(data_date=line['date'].split(" ")[0], simulation=sim.id,
                                               date_output_generated=sim.date_output_generated)

                total_obj.total_low += float(line['value_low'])
                total_obj.total_mid += float(line['value_mid'])
                total_obj.total_high += float(line['value_high'])
                total_obj.save()
            except ObjectDoesNotExist:
                total = Totals.objects.create(
                    data_date=line['date'].split(" ")[0],
                    simulation=sim,
                    total_low=line['value_low'],
                    total_mid=line['value_mid'],
                    total_high=line['value_high'],
                    date_output_generated=sim.date_output_generated
                )
        for sim in simulation_set:
            sim.is_uploaded = True
            sim.save()
    except Exception as e:
        logger.exception('Exception: %s' % e)
        msg = '%s: %s' % ((type(e).__name__), str(e))
        upload_job.status = UploadJob.FAILED
        upload_job.last_error_message = msg
        upload_job.save(update_fields=['status', 'last_error_message'])
        return False, msg

    upload_job.status = UploadJob.COMPLETED
    upload_job.progress = 100
    upload_job.save(update_fields=['status', 'progress'])
    print('Upload complete')
    return True, ""
