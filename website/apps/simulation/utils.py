# Copyright (C) 2016, University of Notre Dame
# All rights reserved
import csv
from website.apps.simulation.models import Location, Simulation, Data


def load_simulation_file(filename, simulation_name):
    fp = open(filename, 'rU')
    dictreader = csv.DictReader(fp)

    simulation = Simulation.objects.create(name=simulation_name)
    line = None
    for line in dictreader:
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