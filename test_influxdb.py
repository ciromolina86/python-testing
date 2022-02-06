import json
import pandas as pd
from influxdb import InfluxDBClient
from datetime import datetime
import numpy as np

# create the influxdb cleint
client = InfluxDBClient('192.168.91.138', 8086, 'root', 'sbrQp10', 'sorba_sde')

# 
from_time = np.datetime64(datetime.strptime("2021-03-22 16:14", "%Y-%m-%d %H:%M").astimezone(),'ns')
from_ts = np.int64(from_time)

#
to_time = np.datetime64(datetime.utcnow(), 'ns')
to_ts = np.int64(to_time)

# influxdb query
result = client.query('select HW___CPU from PC where time >= {} and time <= {}'.format(from_ts, to_ts))
##result = client.query('select HW___CPU from PC order by time desc limit 1')

# print a list of dicts
print(list(result.get_points()))

# create a pandas dataframe
df = pd.DataFrame(list(result.get_points()))

# set time column as dataframe index
df.set_index('time', inplace=True)

# print a dict of dicts as string
print(json.dumps(df.to_dict()))

# print the dataframe shape
print(df.shape)

##with open('D:\\OneDrive - ITG Technologies\\Documents\\_SORBA\\Development\\_Scripts\\result_json.json', 'w') as f:
##    f.write(json.dumps(df.to_dict(), indent=4))

