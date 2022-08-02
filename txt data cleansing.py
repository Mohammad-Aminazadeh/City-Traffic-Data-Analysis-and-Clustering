'''
Description:
-- SCRIPT 1
-- this script is the initial script to run. but before this, allt the file's multi spaces should be converted into a signle 
space, which currently is done by hand. a script should be written for that and should be ran before this script 
(or before this line in the current script)
-- there is no script for eliminating the "n=" format from text files, and since now, all the work has done by hand.
this process should be added to this script.
-- there is no script to change the format of missing values (from numeric 2046, 2047, 14xxx) all to NA.
this process should be added to this script.
'''

import statistics
import os

def get_average(line):
    """getting the average of present values in the line (for missing values)"""
    data_start_index = 3
    return str(int(statistics.mean([int(num) for num in line[data_start_index:] if num != "NA"])))

def reshape_missing_values(data_lines):
    '''
    finds null numbers such as 2046, 2047, 14XXX and replaces them with NA
    '''
    data_start_index = 1
    for i in range(len(data_lines)):
        for j in range(data_start_index, len(data_lines[i])):
            if data_lines[i][j] > 2 * int(get_average(data_lines[i])):
                # this value is suspicious for being null
                data_lines[i][j] = "NA"

    return data_lines


main_directory = 'E://The Project/Data working on/scats-97-99/0-All-2021/new'
for file in os.listdir(main_directory):
    with open(os.path.join(main_directory, file)) as raw_data:


        raw_data_lines = raw_data.readlines()
        '''
        raw_data_lines elements:

        Thursday 01 July 2021 00:15
        Int 1080 1=8 2=32 3=24 4=43 5=74 6=65 7=2 8=70
        9=79 10=57 11=0
        Int 1109 1=26 2=57 3=64 4=46 5=47 6=92 7=0 8=57
        9=0 10=12 11=0 12=19
        '''
        
        edited_data_lines = []
        temp_line = ''


        for i in range(len(raw_data_lines)):
            if "Int" in raw_data_lines[i]:
                # print(temp_line)
                # print('-----------------------')
                # the line contains traffic data
                edited_data_lines.append(temp_line + '\n')

                temp_line = raw_data_lines[i].replace('\n', '')
                # i += 1

                # if "Int" in raw_data_lines[i + 1]:
                #     # the whole data is in a single line
                #     edited_data_lines.append(raw_data_lines[i])
                #     i += 1
                # else:
                #     # the data is diveded into two or more lines
                #     i += 1
            elif "Monday" in raw_data_lines[i] or "Tuesday" in raw_data_lines[i] or "Wednesday" in \
                raw_data_lines[i] or "Thursday" in raw_data_lines[i] or "Friday" in raw_data_lines[i] or \
                    'Saturday' in raw_data_lines[i] or "Sunday" in raw_data_lines[i]:
                # the line contains date and time
                edited_data_lines.append(raw_data_lines[i].replace(" ", "_").replace('\n', '') + '\n')
                # i += 1
            elif "End" in raw_data_lines[i]:
                pass
                # skip the End of file line?
                # i += 1
            else:
                temp_line = temp_line + ' ' + raw_data_lines[i].replace('\n', '')

                

        # for i in range(5):
        #     print(edited_data_lines[i])

        del edited_data_lines[1]
        # print(edited_data_lines)
        # for i in range(5):
        #     print(edited_data_lines[i])
        # replace all "Int" with "#"
        for i in range(len(edited_data_lines)):
            if "Int" in edited_data_lines[i]:
                edited_data_lines[i] = "#" + edited_data_lines[i][4:]
        
        # #1093 1=38 2=53 3=68 4=41 5=62 6=46 7=NA 8=42 9=23 10=68 11=142 12=138\n
        
        new_edited_lines = []
        for line in edited_data_lines:
            if '#' in line:
                split_line = line.split('=')
                # ['#1080 1', '3 2', '10 3', '10 4', '13 5', '31 6', '19 7', '0 8', '25 9', '28 10', '15 11', '2047\n']
                new_line = []
                new_line.append(split_line[0][:-2])
                for i in range(1, len(split_line)-1):
                    new_line.append(split_line[i].split(' ')[0])
                new_line.append(split_line[-1][:-1])
                # ['#1080', '5', '13', '16', '37', '93', '78', '7', '85', '109', '67', '2047']
                new_edited_lines.append(' '.join(new_line) + '\n')
            else:
                new_edited_lines.append(line)

        with open(f"E://The Project/Data working on/scats-97-99/0-All-2021/edited v2/{file}", mode='w')as edited_data:
            # write the new list to new file
            edited_data.writelines(new_edited_lines)
