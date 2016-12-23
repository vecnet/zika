# Script to generate a fake data simulation file
# TO RUN: python generate_fake_data.py output_filename model_name output_generated_date

import decimal
import random
import sys
import uuid

from django.db.models.functions import datetime

# Get the list of arguments
argument_list = (sys.argv)

# Create and open new data file to write to
file_path = '../website/apps/home/data/'
if argument_list[1]:
    file_name = argument_list[1]
else:
    file_name = str(datetime.datetime())
file_to_open = file_path + file_name + '.csv'
data_file = open(file_to_open, 'w')

# Write the header line
data_file.write("name,output_generate_date,value_mid,value_high,disease,model_name,department,"
                "municipality_code,municipality,department_code,date,value_low,id,population\n")

# Open the department and municipality file:
dept_mun_file = open('all_department_municipalities_colombia.csv', 'r')
department_municipality_list = []
for dept_mun in dept_mun_file:
    dept_and_municipality = []
    dm = dept_mun.strip('\n').split(",")
    department_municipality_list.append(dm)

# SET DATA
name = 'suspected cases'

# Check if output_generated_date provided
if argument_list[3]:
    output_generate_date = argument_list[3]
else:
    output_generate_date = str(datetime.datetime.date())

disease = "ZVD"

# Check if model name provided
if argument_list[2]:
    model_name = argument_list[2]
else:
    model_name = "test_model"

date_list = ['2015-08-13', '2015-08-20', '2015-08-27', '2015-09-03', '2015-09-10', '2015-09-17', '2015-09-24',
             '2015-10-01', '2015-10-08', '2015-10-15', '2015-10-22', '2015-10-29', '2015-11-05', '2015-11-12',
             '2015-11-19', '2015-11-26', '2015-12-03', '2015-12-10', '2015-12-17', '2015-12-24', '2015-12-31',
             '2016-01-07', '2016-01-14', '2016-01-21', '2016-01-28', '2016-02-04', '2016-02-11', '2016-02-18',
             '2016-02-25', '2016-03-03', '2016-03-10', '2016-03-17', '2016-03-24', '2016-03-31', '2016-04-07',
             '2016-04-14', '2016-04-21', '2016-04-28', '2016-05-05', '2016-05-12', '2016-05-19', '2016-05-26',
             '2016-06-02', '2016-06-09', '2016-06-16', '2016-06-23', '2016-06-30', '2016-07-07', '2016-07-14',
             '2016-07-21', '2016-07-28', '2016-08-04', '2016-08-11']

population = "all"

for date in date_list:
    dept_mun_line_num = 0
    for item in department_municipality_list:
        if dept_mun_line_num != 0:
            # Generate random data value
            i = random.randint(0, 1)

            value_low = 0
            value_mid = 0
            value_high = 0

            if i == 0:
                value_low = 0
                value_mid = random.random()
                value_high = (decimal.Decimal('%d.%d' % (random.randint(0, 9), random.randint(0, 9999999999999999))))
            elif i == 1:
                value_low = random.random()
                value_mid = int(random.random() * 10)
                while value_mid <= value_low:
                    value_mid = int(random.random() * 10)
                value_high = (decimal.Decimal('%d.%d' % (random.randint(0, 9), random.randint(0, 9999999999999999))))
                while value_high <= value_mid:
                    value_high = (
                    decimal.Decimal('%d.%d' % (random.randint(0, 9), random.randint(0, 9999999999999999))))


            # Generate UUID
            id = (uuid.uuid4())

            line = []
            line.append(name)
            line.append(output_generate_date),
            line.append(value_mid)
            line.append(value_high)
            line.append(disease)
            line.append(model_name)
            line.append(item[1])
            line.append(item[2])
            line.append(item[3])
            line.append(item[0])
            line.append(date)
            line.append(value_low)
            line.append(id)
            line.append(population)

            sim_data_list = ','.join(map(str, line))

            print(sim_data_list + "\n")

            data_file.write(sim_data_list + "\n")
        dept_mun_line_num += 1
