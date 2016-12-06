# This script extracts the department code, department name,
# municipality code, and municipality name from an original data file
# data_cases_combo_new.csv and writes them to a file.

data_file = open('../website/apps/home/data/data_cases_combo_new.csv', 'r')
# write_file = open('department_municipalities_colombia.csv', 'w')

all_dept_municipality_list = []
date_list = []
for line in data_file:
    each_line = line.split(",")
    # dept = [each_line[9], each_line[6]]
    all_dept_municipality_list.append(str(each_line[9]) + "," + each_line[6] + "," + str(each_line[7]) + "," + each_line[8])

    # write_file.write(each_line[9] + "," + each_line[6] + ","
    #                  + each_line[7] + "," + each_line[8] + "\n")
    date_list.append(str(each_line[10])[0:-9])
dept_mun_set = set(all_dept_municipality_list)
all_dept_municipality_list = list(dept_mun_set)

# for item in all_dept_municipality_list:
#     write_file.write(item+"\n")
print(list(set(date_list)))
