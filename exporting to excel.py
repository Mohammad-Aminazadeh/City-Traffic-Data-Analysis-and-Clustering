'''
Description:
-- SCRIPT 4
-- this script exports the data from a text file which contains only a single scat, to its corresponding excel file with
the same name.
-- this script is ran after all scats are seperated, null values are filled, jalali date is added and date and time are 
seperated. in other words, all the process should be done on the text file and this script only exports text to excel.
'''

import pandas as pd
import os

# the main code to create excel files from scratch
# main_directory = "D:\\UNI\\The Project\\Data working on\\scats-97-99\\All scats seperated edited"
# for file in os.listdir(main_directory):
#     with open(os.path.join(main_directory, file)) as data_file:
#         # with open(f"D:\\UNI\\The Project\\Data working on\\scats-97-99\\All scats seperated edited\\Excel Files\\{file[:5]}.xlsx") as scat_excel:
#         data_lines = data_file.readlines()
#         data_lines = [data_line.split() for data_line in data_lines]
#         print(data_lines[0])

#         scat_id = []
#         days = []
#         dates = []
#         times = []
#         traffics = []

#         for line in data_lines:
#             scat_id.append(line[0])
#             days.append(line[1])
#             dates.append(line[2] + " " + line[3] + " " + line[4])
#             times.append(line[5])
#             traffics.append(line[6])

#         data_dict = {"Scat_ID": scat_id,
#                      "Gregorian Date": dates,
#                      "Day": days,
#                      "Time": times,
#                      "Traffic": traffics}

#         data_frame = pd.DataFrame(data_dict, columns = ["Scat_ID", "Gregorian Date", "Day", "Time", "Traffic"])
#         # print(data_frame)

#         data_frame.to_excel(f"D:\\UNI\\The Project\\Data working on\\scats-97-99\\All scats seperated edited\\Excel Files\\{file[:5]}.xlsx", index = False, header = True)
# ==============================================================================================================

# the code to append new data to previous excel files
main_directory = "D://UNI/The Project (New)/Data working on/scats-97-99/4-All Intersections Nulls filled/Without Jalali Date"
for file in os.listdir(main_directory):
    with open(os.path.join(main_directory, file)) as data_file:
        # with open(f"D:\\UNI\\The Project\\Data working on\\scats-97-99\\All scats seperated edited\\Excel Files\\{file[:5]}.xlsx") as scat_excel:
        '''
        data line format:
        #1016 Monday 01 October 2018 01:30 1397-07-09 01:30:00 137 11 
        '''
        data_lines = data_file.readlines()
        data_lines = [data_line.split() for data_line in data_lines]
        print(data_lines[0])
        intersection_id = []
        days_of_the_week = []
        gregorian_dates = []
        times = []
        # jalali_dates = []
        traffic_sums = []
        # traffic_means = []

        for line in data_lines:
            intersection_id.append(line[0])
            days_of_the_week.append(line[1])
            gregorian_dates.append(line[2] + "-" + line[3] + "-" + line[4])
            times.append(line[5])
            # jalali_dates.append(line[6])
            traffic_sums.append(line[6])
            # traffic_means.append(line[9])

        data_dict = {
            "Intersection ID": intersection_id,
            "Gregorian Date": gregorian_dates,
            # "Jalali Date": jalali_dates,
            "Day of The Week": days_of_the_week,
            "Time": times,
            "Traffic Sum": traffic_sums
            # "Traffic Mean": traffic_means
        }

        data_frame = pd.DataFrame(data_dict, columns=["Intersection ID", "Gregorian Date", "Day of The Week", "Time", "Traffic Sum"])
        data_frame.to_csv(f"D://UNI/The Project (New)/Data working on/scats-97-99/5-All Intersection Excel-CSV Files/Without Jalali Date/{file[:5]}.csv", index=False, header=True)
