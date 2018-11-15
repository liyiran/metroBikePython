import glob
import os

import matplotlib.pyplot as plt
import pandas as pd

usage = pd.concat(map(pd.read_csv, glob.glob(os.path.join('data', "*.csv"))))
usage = usage.reset_index(drop=True)
print(len(usage))
# some files use start station but others use start station_id
usage['start_station_id'].fillna(usage['start_station'], inplace=True)
usage['end_station_id'].fillna(usage['end_station'], inplace=True)
usage.drop(['start_station'], axis=1)
usage['start_station_id'] = usage['start_station_id'].astype('category')
# usage['start_time'] = pd.to_datetime(usage['start_time'])
# usage['end_time'] = pd.to_datetime(usage['end_time'])
# print(usage['start_time'][0].strftime("%Y_%m"))
# print(usage['end_time'][0].strftime("%Y_%m"))
station = pd.read_csv("stationdata/metro-bike-share-stations-2018-10-19.csv")
station['Station_ID'] = station['Station_ID'].astype('category')
print(len(station))

bigTabe = pd.merge(usage, station, how='inner', left_on='start_station_id', right_on='Station_ID')
bigTabe['start_station_id'] = bigTabe['start_station_id'].astype('category')
print(len(bigTabe))

dtlaUsage = bigTabe.query('Region == "Pasadena"').groupby(['start_station_id']).size().reset_index(name='count').set_index('start_station_id').query('count > 0')
print(dtlaUsage)
dtlaUsage.plot(kind="bar")
plt.show()
