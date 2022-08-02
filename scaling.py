'''
this script changes the scale of the data and zooms it out from 15 minute periods to 1 day periods
CSV files are created next
'''

import os
import pandas as pd


def get_daily_scale(data_lines):
    '''
    returns data lines in daily scale: each record is one day.
    '''
    days = {}
    daily_data_lines = []

    for i in range(len(data_lines)):
        # print(data_lines[i])
        # ['#1001', 'Sunday', '28', 'October', '2018', '12:00', '746']
        if data_lines[i][-1] != "NA" and data_lines[i][-1] != "0":
            # line's traffic is not null
            current_key = f"{data_lines[i][0]} {data_lines[i][1]} {data_lines[i][2]} {data_lines[i][3]} {data_lines[i][4]}"
            current_traffic = int(data_lines[i][-1])
            if current_key in days.keys():
                days[current_key] += current_traffic
            else:
                days[current_key] = current_traffic

    for key, value in days.items():
        daily_data_lines.append(f"{key} {value}")
        # print (f"{key} {value}")

    daily_data_lines = [line.split() for line in daily_data_lines]
    return daily_data_lines


def get_month_number(month):
    '''
    maps month's name to month's number
    '''
    map_dict = {
        "January": 1,
        "February": 2,
        "March": 3,
        "April": 4,
        "May": 5,
        "June": 6,
        "July": 7,
        "August": 8,
        "September": 9,
        "October": 10,
        "November": 11,
        "December": 12
    }
    return map_dict[month]


# ========================================================================================================================
if __name__ == "__main__":

    # iterating through all monthly files and seperating the data_ids into new files.
    main_directory = "D://UNI/The Project (New)/Data working on/scats-97-99/4-All Intersections Nulls filled/Without Jalali Date"
    for file in os.listdir(main_directory):
        with open(os.path.join(main_directory, file)) as data_file:

            data_lines = data_file.readlines()
            '''
            Data line format:
            ['#1001', 'Monday', '01', 'October', '2018', '00:15', '352']

            Intersection Seperation by Year Data line format:
            ['#1002', 'Tuesday_01_January_2019_00:15', '212']
            '''
            data_lines = [data_line.split() for data_line in data_lines]
            print(data_lines[0])

            # changing the scale of data
            data_lines = get_daily_scale(data_lines)
            print(data_lines[0])
            
            # preparing data to export to excel
            intersection_IDs = []
            days_of_the_week = []
            gregorian_dates = []
            # jalali_dates = []
            traffic_sums = []

            for line in data_lines:
                intersection_IDs.append(line[0])
                
                # line_date_time = line[1].split('_')
                days_of_the_week.append(line[1])
                # print(line_date_time)
                gregorian_dates.append(f"{line[4]}-{get_month_number(line[3])}-{line[2]}")
            #     jalali_dates.append(line[5])
                traffic_sums.append(line[-1])

            data_dict = {
                "Intersection ID": intersection_IDs,
                "Gregorian Date": gregorian_dates,
            #     "Jalali Date": jalali_dates,
                "Day of The Week": days_of_the_week,
                "Traffic Sum": traffic_sums
            }

            traffic_df = pd.DataFrame(data_dict, columns=["Intersection ID", "Gregorian Date", "Day of The Week", "Traffic Sum"])
            
            traffic_df.to_csv(f"D://UNI/The Project (New)/Data working on/scats-97-99/6-Daily Scaled CSV Files/{file[:5]}.csv", index=False, header=True)

