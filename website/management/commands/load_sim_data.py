# Copyright (C) 2017, University of Notre Dame
# All rights reserved
import csv
import os

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from django.db import transaction

from website.apps.home.models import Simulation, Location, Data, SimulationModel, Totals


class Command(BaseCommand):
    help = 'Upload csv data file and save objects in database'

    def add_arguments(self, parser):
        parser.add_argument("sim_id", type=int)

    def handle(self, *args, **options):
        """
        Upload data file
        :param args:
        :param options:
        :return:
        """

        sim_id = options["sim_id"]
        sim = Simulation.objects.get(id=sim_id)

        filename = os.path.join(settings.MEDIA_ROOT, sim.data_file.name)

        file_obj = open(filename, 'r')

        dictreader = csv.DictReader(file_obj)
        line = None

        for line in dictreader:
            # Get or Create the SimulationModel object
            if line['model_name'] is not None:
                model_obj = SimulationModel.objects.get_or_create(model_name=line['model_name'])
                sim.sim_model_id = model_obj[0].id

            sim.date_output_generated = line['output_generate_date']

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
                print("WARNING: department name mismatch (%s, %s)" % (location.department, line['department']))

            if location.municipality != line['municipality']:
                print("WARNING: municipality name mismatch (%s, %s)" % (location.municipality, line['municipality']))

            Data.objects.create(
                location=location,
                date=line['date'].split(" ")[0],  # Assuming date is in "YYYY-MM-DD HH:MM:SS" format
                simulation=sim,
                value_low=line['value_low'],
                value_mid=line['value_mid'],
                value_high=line['value_high'],
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

        sim.is_uploaded = True
        sim.save()

