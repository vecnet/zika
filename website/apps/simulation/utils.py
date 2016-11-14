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

import csv

import logging

from website.apps.simulation.models import Location, Simulation, Data

logger = logging.getLogger(__name__)


def load_simulation_file(fp, simulation_name):
    read_file = open(fp.file.name, 'r')
    dictreader = csv.DictReader(read_file)

    simulation = Simulation.objects.create(name=simulation_name)
    line = None

    print("-------------------- IN LOAD SIM FILE! --------------------")

    for line in dictreader:
        print(line)
        print("!!!!!!!!!!!!!!!")
        location = Location.objects.filter(
            department_code=line['department_code'],
            municipality_code=line['municipality_code'],
        ).first()

        if not location:
            location = Location.objects.create(
                department=line['department'],
                department_code=line['department_code'],
                municipality=line['municipality'],
                municipality_code=line['municipality_code'],
            )
        if location.department != line['department']:
            print("WARNING: deparment name mismatch (%s, %s)" % (location.department, line['department']))

        if location.municipality != line['municipality']:
            print("WARNING: municipality name mismatch (%s, %s)" % (location.municipality, line['municipality']))

        Data.objects.create(
            location=location,
            date=line['date'].split(" ")[0],  # Assuming date is in "YYYY-MM-DD HH:MM:SS" format
            simulation=simulation,
            value_low=line['value_low'],
            value_mid=line['value_mid'],
            value_high=line['value_high'],
        )

    if line:
        # Non-empty simulation output file
        simulation.model_name = line['model_name']
        # simulation.date_output_generated = line['output_generate_date']
        simulation.save()
