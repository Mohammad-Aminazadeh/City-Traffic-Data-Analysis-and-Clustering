'''
this script merges the weather dataset with traffic datasets
'''

import os
import statistics
import jdatetime
from numpy.lib.ufunclike import fix
import pandas as pd
from pandas.core import frame


def fix_date(data_lines, mode):
    '''
    fixes date to be exactly in the form of YYYY-MM-DD not YYYY-M-DD or YYYY-MM-D
    mode 0 for weather list
    mode 1 for traffic list
    '''
    for i in range(len(data_lines)):
        date = data_lines[i][mode]
        date = date.split('-')
        print(data_lines[i])
        # print(i)
        if len(date[1]) == 1:
            date[1] = f"0{date[1]}"

        if len(date[2]) == 1:
            date[2] = f"0{date[2]}"

        data_lines[i][mode] = "-".join(date)
    return data_lines

# ========================================================================================================================
if __name__ == "__main__":

    '''
    weather df format:
             Date        wind avg peed    max temperature  min temperature   last 24 hour rain       last 24 hour sunny hours
    0     9/22/2018        2.37500             31.8             15.6                0.0                       9.6

    traffic df format:
         Intersection IC  Gregorian Date        Jalali Date        Day of The Week     Traffic Sum
    0       #1002          2018-10-01           1397-07-09             Monday            41106
    '''

    # iterating through all monthly files and seperating the data_ids into new files.
    main_directory = "D:\\UNI\\The Project\\Data working on\\scats-97-99\\6-Daily Scaled CSV Files"
    for file in os.listdir(main_directory):
        
        traffic_df = pd.read_csv(f"{main_directory}\\{file}")
        weather_df = pd.read_csv("D:\\UNI\\The Project\\Data working on\\External Data\\Weather Data.csv")

        print(traffic_df)
        print("========================================================================================")
        

        weather_list = weather_df.values.tolist()
        traffic_list = traffic_df.values.tolist()

        # changing weather date format to YYYY-MM-DD
        for i in range(len(weather_list)):
            date = weather_list[i][0].split("/")
            new_date = f"{date[2]}-{date[0]}-{date[1]}"
            weather_list[i][0] = new_date


        weather_list = fix_date(weather_list, 0)
        traffic_list = fix_date(traffic_list, 1)
        

        # converting weather list to df
        gregorian_dates = []
        wind_avg_speeds = []
        max_temperature = []
        min_temperature = []
        rain = []
        sunny_hours = []

        for line in weather_list:
            gregorian_dates.append(line[0])
            wind_avg_speeds.append(line[1])
            max_temperature.append(line[2])
            min_temperature.append(line[3])
            rain.append(line[4])
            sunny_hours.append(line[5])

        weather_dict = {
            "Gregorian Date": gregorian_dates,
            "Wind AVG Speed": wind_avg_speeds,
            "Max Temp": max_temperature,
            "Min Temp": min_temperature,
            "Rain": rain,
            "Sunny Hours": sunny_hours
        }

        weather_df = pd.DataFrame(weather_dict, columns=["Gregorian Date", "Wind AVG Speed", "Max Temp", "Min Temp", "Rain", "Sunny Hours"])
        print(weather_df)
        print("========================================================================================")


        # convert traffic list to df
        intersection_IDs = []
        gregorian_dates = []
        jalali_dates = []
        days_of_week = []
        traffic_sums = []

        for line in traffic_list:
            intersection_IDs.append(line[0])
            gregorian_dates.append(line[1])
            jalali_dates.append(line[2])
            days_of_week.append(line[3])
            traffic_sums.append(line[4])

        traffic_dict = {
            "Intersection ID": intersection_IDs,
            "Gregorian Date": gregorian_dates,
            "Jalali Date": jalali_dates,
            "Day of The Week": days_of_week,
            "Traffic Sum": traffic_sums
        }

        traffic_df = pd.DataFrame(traffic_dict, columns=["Intersection ID", "Gregorian Date", "Jalali Date", "Day of The Week", "Traffic Sum"])

        # df inner join
        result = pd.merge(traffic_df, weather_df, how="inner")
        print(result)

        result.to_csv(f"D:\\UNI\\The Project\\Data working on\\scats-97-99\\7-Merged With Weather Excels\\{file}", index=False, header=True)
        