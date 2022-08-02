'''
Description:
this file is to run test codes and check different functionalities.
'''

# import jdatetime
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from pyparsing import col
import seaborn as sns
sns.set()
from tslearn.preprocessing import TimeSeriesScalerMeanVariance
from tslearn.clustering import TimeSeriesKMeans

# loading year 2019 data file
main_directory = 'D://UNI/The Project (New)/Data working on/scats-97-99/6-Daily Scaled CSV Files'
intersection_IDs = []
shapes = {}
traffic_time_series = []
intersection_dict = {}
max_time_series_length = 0
for file in os.listdir(main_directory):
    # print(file)
    if file in ['#1043.csv', '#1017.csv', '#1075.csv']:
        continue
    with open(os.path.join(main_directory, file)) as data_file:
        data_frame = pd.read_csv(data_file)
        current_id = data_frame['Intersection ID'].iloc[0]
        intersection_IDs.append(current_id)
        
        # Max dataframe length = 1097
        vertical_traffics = data_frame['Traffic Sum']
        
        
        # remove the outliers from time serie values
        q1 = vertical_traffics.quantile(0.95)
        vertical_traffics = vertical_traffics[vertical_traffics < q1]

        q2 = vertical_traffics.quantile(0.05)
        vertical_traffics = vertical_traffics[vertical_traffics > q2]

        # print(f"temp vert size after: {vertical_traffics.shape}")

        # vertical_traffics = vertical_traffics[vertical_traffics > 6*1/vertical_traffics]
        # add time series with lenght above 750 only to eliminate intersections with too short time series

        
        # add zeroes at the end of time series to reach length 1097
        vertical_traffics_list = list(vertical_traffics)
        for i in range(1097-len(vertical_traffics_list)):
            vertical_traffics_list.append(0)
        # print(vertical_traffics_list)
        # print('======================================')
        temp_vertical_traffics = pd.DataFrame({'Traffic Sum': vertical_traffics_list})
        vertical_traffics = temp_vertical_traffics['Traffic Sum']
        # print(vertical_traffics.shape)
        # print("=====================================")

        intersection_dict[f'{current_id}'] = vertical_traffics


# print(time_series_matrix)
# print(time_series_matrix.shape)

# Normalizing the data
# time_series_matrix = TimeSeriesScalerMeanVariance().fit_transform(time_series_matrix)
# print(f'====================Max: {max_time_series_length}====================')

#---------------------------------------Summary Tables---------------------------------------
summary_table_df = pd.read_excel('D://UNI/The Project (New)/Data working on/scats-97-99/8-Clustering Results/Euclidean Summary Table.xlsx')
# print(summary_table_df.head())
'''
      ID  Cluster
0  #1016        0
1  #1051        0
2  #1054        0
3  #1068        0
4  #1069        0
'''
intersections = list(summary_table_df['ID'])
labels = list(summary_table_df['Cluster'])



# remove all zeros from all time series to prepare for plotting
for i in range(len(intersection_IDs)):
    current_time_series = intersection_dict[intersection_IDs[i]]
    intersection_dict[intersection_IDs[i]] = [e for e in intersection_dict[intersection_IDs[i]] if e != 0]
    


# plotting time series of a single cluster
for i in range(len(labels)):
    if labels[i] == 3:
        plt.plot(intersection_dict[intersections[i]])

plt.title('Cluster #4')
plt.xlabel('Day')
plt.ylabel('Number of Vehicles')
# while True:
#     pass
plt.show()