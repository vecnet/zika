import os
import csv
import random

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def produce_new_data_combo_case():
    fp = open(os.path.join(BASE_DIR, 'website', 'apps', 'simulation', 'data', 'data_cases_combo_20160810.csv'), 'rU')
    dictreader = csv.DictReader(fp)
    data = []
    row = {}
    for row in dictreader:
        if float(row["value_mid"]) > 0:
            row["value_low"] = float(row["value_mid"])*0.7
            row["value_high"] = float(row["value_mid"])*1.5
        else:
            row["value_low"] = 0
            row["value_high"] = random.random()*3
        data.append(row)
    fp.close()

    fp = open(os.path.join(BASE_DIR, 'website', 'apps', 'simulation', 'data', 'data_cases_combo_new.csv'), 'wb')
    dictwriter = csv.DictWriter(fp, fieldnames=row.keys())
    dictwriter.writeheader()
    for row in data:
        dictwriter.writerow(row)
    fp.close()


if __name__ == '__main__':
    produce_new_data_combo_case()
