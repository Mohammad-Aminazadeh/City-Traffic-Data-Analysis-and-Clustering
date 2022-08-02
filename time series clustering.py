'''
Description:
this file is to run test codes and check different functionalities.
'''

from cProfile import label
from datetime import datetime
from email import header
from operator import index
from cffi import VerificationError
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


        traffic_time_series.append(vertical_traffics)
        intersection_dict[f'{current_id}'] = vertical_traffics


time_series_matrix = np.row_stack(traffic_time_series)
# print(time_series_matrix)
# print(time_series_matrix.shape)

# Normalizing the data
# time_series_matrix = TimeSeriesScalerMeanVariance().fit_transform(time_series_matrix)
# print(f'====================Max: {max_time_series_length}====================')
#---------------------------------------K Means Methods----------------------------------------
wcss = []

# Euclidean K Means
# km = TimeSeriesKMeans(n_clusters=5, metric="euclidean", verbose=True, random_state=36)
# km.fit(time_series_matrix)

# DBA K Means
# km = TimeSeriesKMeans(n_clusters=5,
#                           n_init=2,
#                           metric="dtw",
#                           verbose=True,
#                           max_iter_barycenter=10,
#                           random_state=36)
# km.fit(time_series_matrix)

# calculating the best number of clusters with the elbow method (minimum WCSS with least number of clusters)

# Soft DTW K Means
# km = TimeSeriesKMeans(n_clusters=5,
#                            metric="softdtw",
#                            metric_params={"gamma": .01},
#                            verbose=True,
#                            random_state=36)
# km.fit(time_series_matrix)
# ------------------------------------------The Elbow Method-----------------------------------
# The Elbow Method for Euclidean K Means
for counter in range(1, 10):
    km = TimeSeriesKMeans(n_clusters=counter,
                        n_init=3,
                        metric="euclidean",
                        verbose=True,
                        max_iter_barycenter=10,
                        random_state=36)
    km.fit(time_series_matrix)
    wcss.append(km.inertia_)
plt.title('Elbow Method for Euclidean K-Means')
plt.xlabel('Number of Clusters')
plt.ylabel('WCSS')
plt.plot(wcss)

# The Elbow Method for DBA K Means
# for counter in range(1,15):
#     dba_km = TimeSeriesKMeans(n_clusters=counter,
#                         n_init=2,
#                         metric="dtw",
#                         verbose=True,
#                         max_iter_barycenter=10,
#                         random_state=36)
#     dba_km.fit(time_series_matrix)
#     wcss.append(dba_km.inertia_)
# plt.title('Elbow Method for DBA K-Means')
# plt.xlabel('Number of Clusters')
# plt.ylabel('WCSS')
# plt.plot(wcss)

# The Elbow Method for Soft DTW K Means
# for counter in range(1, 6):
#     sdtw_km = TimeSeriesKMeans(n_clusters=counter,
#                            metric="softdtw",
#                            metric_params={"gamma": .01},
#                            verbose=True,
#                            random_state=36)
#     sdtw_km.fit(time_series_matrix)
#     wcss.append(sdtw_km.inertia_)
# plt.title('Elbow Method for Soft DTW K-Means')
# plt.xlabel('Number of Clusters')
# plt.ylabel('WCSS')
# plt.plot(wcss)

# plotting clusters
# 1- make a dictionary of each intersection ID and its relative time serie to access to them later
# 2- plot each cluster's intersection on a single chart
# 3- display all the charts beside each other

#---------------------------------------Summary Tables---------------------------------------

# creating a summary table for Euclidean K Means
summary_table = pd.DataFrame()
summary_table['ID'] = intersection_IDs
summary_table['Cluster'] = km.labels_
#-----------------------------------Summary Table to Excel-----------------------------------

# Euclidean K Means
# summary_table.to_excel("D://UNI/The Project (New)/Data working on/scats-97-99/8-Clustering Results/New Euclidean Summary Table.xlsx", index=False, header=True)


# remove all zeros from all time series to prepare for plotting
# for i in range(len(intersection_IDs)):
#     current_time_series = intersection_dict[intersection_IDs[i]]
#     intersection_dict[intersection_IDs[i]] = [e for e in intersection_dict[intersection_IDs[i]] if e != 0]
    

# plotting time series of a single cluster
# for i in range(0,len(km.labels_)):
#     if km.labels_[i] == 4:
#         plt.plot(intersection_dict[intersection_IDs[i]])
# plt.title('Cluster #5')
# plt.xlabel('Day')
# plt.ylabel('Number of Vehicles')

plt.show()