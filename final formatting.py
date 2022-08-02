'''
Description:
-- SCRIPT 3 (Filling Missing values)
-- this script is ran after the Scat id seperation script.
-- this script fills the missing values.
-- this script seperates date and time into different attributes in a line.
'''

import os
import statistics
import jdatetime
from pandas.core.frame import DataFrame
from math import floor
import pandas as pd

# import plotly.express as px


# def get_variance(line1, line2):
#     '''
#     returns the average variance of two given lines as a number. the less it is, the more similar the lines are.
#     because line lenghts could be different, the lower lenght values of each lines are taken into account.
#     '''
#     variance = []

#     # in the data lines the traffic values start at index 3
#     data_start_index = 3
#     line1_len = len(line1[data_start_index:])
#     line2_len = len(line2[data_start_index:])

#     for i in range(min(line1_len, line2_len)):
#         variance.append(
#             abs(int(line1[data_start_index + i]) - int(line2[data_start_index + i])))
#     return sum(variance) / len(variance)


# def get_days_of_week_variance(data_lines):
#     '''
#     this function calculates the average variance of values in same days of the week over different weeks.
#     the step over lines to jump to the same day of the next week is 672.
#     the step over lines to jump to the same time of the next day is 96

#     line format:
#     ['#1002', 'Tuesday 16 October 2018 15:45', '1397-07-24 15:45:00', '41', '40', '45', '21', '43', '31', 'NA', '49', '46', '19', '37', '31', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '403']
#     '''

#     next_week_step = 672
#     next_day_step = 96
#     days_of_the_week_variances = {
#         "Monday": [],
#         "Tuesday": [],
#         "Wednesday": [],
#         "Thursday": [],
#         "Friday": [],
#         "Saturday": [],
#         "Sunday": []
#     }
#     line_date_times = [line[1].split() for line in data_lines]

#     # the main loop that jumps over the next pair of weeks (jumps 2 weeks at a time)
#     for i in range(0, len(data_lines) - 2 * next_week_step, 2 * next_week_step):
#         for j in range(i, i + next_week_step):

#             k = j + next_week_step
#             if not line_has_null(data_lines[j]) and not line_has_null(data_lines[k]):

#                 day_of_the_week = line_date_times[j][0]

#                 days_of_the_week_variances[day_of_the_week].append(
#                     get_variance(data_lines[j], data_lines[k]))

#     return days_of_the_week_variances


def get_missings (data_lines):
    for i in range(len(data_lines)):
        for j in range(len(data_lines[i])):
            if data_lines[i][j] == "2046" or data_lines[i][j] == "2047" or data_lines[i][j] == "0":
                data_lines[i][j] = "NA"
    return data_lines

def get_average(line):
    """getting the average of present values in the line (for missing values)"""
    data_start_index = 2
    # print(line)
    try:
        return str(int(statistics.mean([int(num) for num in line[data_start_index:] if num != "NA"])))
    except:
        return 0


def line_has_null(line):
    '''returns true if there is one or more missing values in the line. otherwise returns False'''
    data_start_index = 2
    if "NA" in line[data_start_index:]:
        return True 
    return False


def line_is_null(line):
    """returns true if the whole line is null. otherwise returns False"""
    # index 3 and after are reserved ro data
    data_start_index = 2
    threshold = 0.6
    if line[data_start_index:].count('NA') > floor(threshold*len(line[data_start_index:])):
        return True
    return False


# def get_sum(line):
#     """
#     returns the sum of present values of the line
#     """
#     data_start_index = 3
#     return str(sum([int(num) for num in line[data_start_index:]]))


def join_date_time(data_lines, mode):
    '''
    joins the date and time with adding "_" rather than" " for jalali and gregorian date_time
    if mode = "gregorian", it joins the date and time with '_'
    if mode = "jalali", it joins the date and time with '-'
    '''
    if mode == "gregorian":
        for i in range(len(data_lines)):
            data_lines[i][1] = data_lines[i][1].replace(" ", "_")
    else:
        for i in range(len(data_lines)):
            data_lines[i][2] = data_lines[i][2].replace(" ", "_")

    return data_lines


def date_time_division(data_lines, mode):
    '''
    Seperates the elements of date and time
    if mode = "gregorian", it divides the gregorian date in line
    if mode = "jalali", it divides the jalali date in line
    '''
    if mode == "gregorian":
        for i in range(len(data_lines)):
            data_lines[i][1] = data_lines[i][1].replace("_", " ")
    else:
        for i in range(len(data_lines)):
            data_lines[i][2] = data_lines[i][2].replace("-", " ")
    return data_lines




def remove_corrupted_sensors(data_lines):
    '''
    removes sensors that does not exist and always return wrong/missing values.
    '''
    # corrupted_sensors_df = pd.read_excel('E://The Project/Data working on/scats-97-99/Corrupted Sensors.xlsx')
    # intersection_ids = list(corrupted_sensors_df['Intersection ID'])

    corrupted_sensors_dict = {}
    # corrupted_sensors_dict['#1002'] = [[corrupted_sensors_indices], [max_len]]
    corrupted_sensors_dict['#1002'] = [7]
    corrupted_sensors_dict['#1010'] = [3]
    corrupted_sensors_dict['#1031'] = [4, 8, 12]
    corrupted_sensors_dict['#1032'] = [8]
    corrupted_sensors_dict['#1035'] = [12]
    corrupted_sensors_dict['#1036'] = [3, 6]
    corrupted_sensors_dict['#1038'] = [8]
    corrupted_sensors_dict['#1054'] = [5]
    corrupted_sensors_dict['#1064'] = [3]
    corrupted_sensors_dict['#1066'] = [1]
    corrupted_sensors_dict['#1074'] = [1]
    corrupted_sensors_dict['#1078'] = [4]
    corrupted_sensors_dict['#1083'] = [6]
    corrupted_sensors_dict['#1085'] = [14]
    corrupted_sensors_dict['#1094'] = [11, 12, 13]
    corrupted_sensors_dict['#1109'] = [7, 11]
    corrupted_sensors_dict['#1502'] = [9]
    


    data_start_index = 2
    intersection_id = data_lines[0][0]
    
    for i in range(len(data_lines)):
        # cutting extra end of the intersection
        # data_lines[i] = data_lines[i][0:data_start_index+corrupted_sensors_dict[intersection_id][1][0]]
        if intersection_id == '#1002':
            del data_lines[i][-12:]

        # removing corrupted indices from lines
        if intersection_id in corrupted_sensors_dict.keys():
            # for index in corrupted_sensors_dict[intersection_id]:
            #     del data_lines[i][data_start_index-1+index]

            temp = data_lines[i]
            data_lines[i] = [element for element in temp if temp.index(element) not in [data_start_index-1+index for index in corrupted_sensors_dict[intersection_id]]]
    return data_lines


def add_jalali_date(data_lines):
    '''for each line, adds the corresponding jalali date after gregorian date'''

    # a dictionary for mapping name of the months to number of the months
    months_of_year = {
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

    previous_line_datetime = ""

    for i in range(len(data_lines)):
        '''
        line_datetime format:
        Monday 01 October 2018 02:45

        jalali datetime format:
        1397-08-08 00:00:00
        '''

        try:
            line_datetime = data_lines[i][1].rsplit()
            # print(line_datetime)
            gregorian_datetime = jdatetime.datetime(
                int(line_datetime[3]), int(months_of_year[line_datetime[2]]), int(line_datetime[1]), int(line_datetime[4][0:2]), \
                    int(line_datetime[4][3:]))

            jalali_datetime = jdatetime.datetime.fromgregorian(
                date=gregorian_datetime)

            data_lines[i].insert(2, str(jalali_datetime))
            # print(data_lines[i])
        except ValueError:
            if (previous_line_datetime == ""):
                previous_line_datetime = data_lines[i - 1][1].rsplit()

            previous_gregorian_datetime = jdatetime.datetime(
                int(previous_line_datetime[3]), int(months_of_year[previous_line_datetime[2]]), int(previous_line_datetime[1]), \
                    int(previous_line_datetime[4][0:2]), int(previous_line_datetime[4][3:]))

            previous_jalali_datetime = jdatetime.datetime.fromgregorian(
                date=previous_gregorian_datetime)

            current_jalali_datetime = f"{previous_jalali_datetime.year}-{previous_jalali_datetime.month}-{previous_jalali_datetime.day} \
                {previous_jalali_datetime.hour}:{previous_jalali_datetime.minute}:{previous_jalali_datetime.second}"

            data_lines[i].insert(2, current_jalali_datetime)
            # print(data_lines[i])
    return data_lines


def fill_missing_values(data_lines):
    '''
    fills all the null values
    at the end of each line
    '''
    data_start_index = 2
    last_repaired_line_index = 0

    for i in range(len(data_lines)):
        if not line_is_null(data_lines[i]):
            for j in range(data_start_index, len(data_lines[i])):
                if data_lines[i][j] == "NA":
                    data_lines[i][j] = get_average(data_lines[i])

    return data_lines


def aggregate_data(data_lines):
    '''
    this method, aggregates the values to single values, which are sum and average traffic passed.
    sum and average are added to end of each line.
    '''
    data_start_index = 2
    for i in range(len(data_lines)):
        temp_line = []
        if not line_is_null(data_lines[i]):
            
            temp_line = data_lines[i][0:data_start_index]
            temp_line.append(str(sum([int(num) for num in data_lines[i][data_start_index:]])))
            # temp_line.append(str(int(statistics.mean([int(num) for num in data_lines[i][data_start_index:]]))))
            data_lines[i] = temp_line
        else:
            temp_line = data_lines[i][0:data_start_index]
            temp_line.append(str(0))
            data_lines[i] = temp_line
    return data_lines

# ========================================================================================================================
if __name__ == "__main__":

    # iterating through all monthly files and seperating the data_ids into new files.
    main_directory = "D://UNI/The Project (New)/Data working on/scats-97-99/2-All Intersections with Nulls"
    for file in os.listdir(main_directory):
        with open(os.path.join(main_directory, file)) as data_file:

            data_lines = data_file.readlines()
            data_lines = data_lines[:-2]
            '''
                data_lines format:
                ['#1001', 'Monday_01_October_2018_02:45', '1', '2', '1', '10', '17', '9', 'NA', '4', '2', '0', '4', '3', '53']

                data_lines format after datetime division:
                ['#1001', 'Monday 01 October 2018 02:45', '1', '2', '1', '10', '17', '9', 'NA', '4', '2', '0', '4', '3', '53']

                data_lines format after adding jalali date:
                ['#1002', 'Tuesday 16 October 2018 15:45', '1397-07-24 15:45:00', '41', '40', '45', '21', '43', '31', 'NA', '49', '46', '19', '37', '31', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '403']
                '''

            data_lines = [data_line.split() for data_line in data_lines]

            print(data_lines[0][0])

            

            # datetime division in each line
            data_lines = date_time_division(data_lines, "gregorian")

            # adding jalali date to each line
            # data_lines = add_jalali_date(data_lines)
            print(data_lines[0])
            
            # fixing corrupted sensor indices
            data_lines = remove_corrupted_sensors(data_lines)
            print(data_lines[0])

            # replace 2046 and 2047 with NA
            data_lines = get_missings(data_lines)
            print(data_lines[0])

            # filling missing values
            data_lines = fill_missing_values(data_lines)
            print(data_lines[0])

            # aggregate traffic values to average and sum
            data_lines = aggregate_data(data_lines)
            print(data_lines[0])

            print('-----------------------------------------------------')

            # writing the lines to a new file
            with open(f"D://UNI/The Project (New)/Data working on/scats-97-99/4-All Intersections Nulls filled/Without Jalali Date/{file}", mode='w') as new_file:
                for line in data_lines:
                    new_file.writelines(" ".join(line[:]) + " " + "\n")
