'''
this script reads files of all intersections and plots their time series at once on a single plane. for a 
single intersection, the average value of all days is used.

the average time series of all 71 intersections will be used as a benchmark to compare different intersections' 
time series with.
'''

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
import numpy as np


main_directory = ""