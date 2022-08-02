'''
Description:
-- SCRIPT 2
-- this script seperates all scats into different files containing only single scat id from all months.
-- this script also adds the date and time in the single line above data values, to all corresponding lines seperately.
-- this script sums all the values in a line and adds at the end of the line (this should be changed into different 
directions in an intersection which can be 3 way (3 sum values) or 4 way (4 sum value))
-- this script is ran after the txt data cleaning file
'''

import os
from collections import defaultdict


# all_data_lines = []
intersections_dict = defaultdict(dict)

flag2 = True
main_directory = "E://The Project\Data working on/scats-97-99/1-All Months Toghether/Monthly Separated/2021/1-All Months Together"
for file in os.listdir(main_directory):
    with open(os.path.join(main_directory, file)) as data:
        scat_id_list = []
        flag1 = True
        
        data_lines = data.readlines()
        data_lines_splitted = [line.split() for line in data_lines]
        '''
        data_lines format:
        
        Monday_01_October_2018_00:15
        #1080 15 25 27 41 92 0 0 92 90 37 24
        #1109 30 48 63 54 43 96 0 45 0 5 0 27
        #1081 12 36 36 11 22 20 15 39 36 16 23 0
        #1093 35 51 67 18 44 29 21 30 16 32 56 63
        '''
        new_data_lines = []
        

        # storing the last date_time line into this variable to insert into all lines belonging to this date_time
        current_date_time = ""
        for line in data_lines_splitted:
            temp_line = line
            if len(line) == 1:
                # The line is a date
                current_date_time = line
            else:
                # The line contains numeric data

                # add current date_time to the data line
                temp_line.insert(1, current_date_time[0])

            new_data_lines.append(temp_line)
        # print(new_data_lines)


        # filling the scat_id list with all present unique scat_ids
        for line in new_data_lines:
            if len(line)>1 and line[0] not in scat_id_list:
                # print(line[0])
                scat_id_list.append(line[0])

        # flag1 = False


        # if flag2:
        for id in scat_id_list:
            if id not in intersections_dict.keys():
                intersections_dict[id] = []
                # print(intersections_dict.items())
        # flag2 = False

        for line in new_data_lines:
            if len(line)>1:
                # if (line[0] == "#1071"):
                #     intersections_dict[f'{line[0]}'].append(' '.join(line[:18]) + '\n')
                # else:
                intersections_dict[f'{line[0]}'].append(' '.join(line) + '\n')


for id in scat_id_list:
    with open(f"E:/The Project/Data working on/scats-97-99/1-All Months Toghether/Monthly Separated/2021/2-All Intersections with Nulls/{id}.txt", mode='a') as intersection_file:
        print(f"{id}.txt")
        
        intersection_file.writelines(intersections_dict[f'{id}'])
        intersection_file.write('\n')