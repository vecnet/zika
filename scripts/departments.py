# Copyright (C) 2016, University of Notre Dame
# All rights reserved
import csv
import os

if __name__ == '__main__':
    files = os.listdir("d:\Repositories\zikadata\Colombia\Municipality_Zika\data")

    bydate = {}
    csvdata = []
    for filename in files:
        fp = open("d:\Repositories\zikadata\Colombia\Municipality_Zika\data\%s" % filename, "rU")
        dictreader = csv.DictReader(fp)
        data = {}
        total = 0
        for row in dictreader:
            department = row["location"].split("-")[1]
            if row["data_field"] == "zika_suspected":
                if department not in data:
                    data[department] = 0
                try:
                    data[department] += int(row["value"])
                except ValueError:
                    print row["location"], row["value"]

                total += data[department]
        fp.close()
        bydate[filename] = data
        date = filename.strip("Municipality_Zika_")
        date = date.strip(".csv")
        print date, total

        for item in data:
            date = filename.strip("Municipality_Zika_")
            date = date.strip(".csv")
            item2 = {"location": item, "cases": data[item], "date": date}
            csvdata.append(item2)

    print csvdata

