import time
from datetime import datetime
import numpy as np

########################################

# get local now datetime with timezone
time0 = datetime.now().astimezone()
print('time0: ', time0)
print(time0.tzname())

# convert to numpy datetime64 (UTC)
time0_utc = np.datetime64(time0, 'ns')
print(time0_utc)
print(np.int64(time0_utc))
##print(np.int64(np.datetime64(datetime.utcnow(), 'ns')))


# local datetime
time1 = datetime.strptime("2021-03-22 16:10", "%Y-%m-%d %H:%M").astimezone()
##time1 = time1.astimezone()
print('time1: ', time1)

# convert to numpy datetime64 (UTC)
time1_utc = np.datetime64(time1, 'ns')
print(time1_utc)

# ================================================================================

import pandas as pd

# Read csv
pdf = pd.read_csv("C:\\Users\cmolina\\Desktop\\_MyFiles\\_SORBA files\\Task #1\\test_ds.csv", delimiter=',')

# Transform timestamp to datetime64[ns] data type
pdf['TS'] = pd.to_datetime(pdf['TS'], infer_datetime_format=True)

# Convert timestamp column (datatype: datetime64[ns]) to format: 2017-08-22 13:25:28.875 (datatype: str object)
pdf['TS'] = pdf['TS'].dt.strftime("%Y-%m-%d %H:%M:%S.%f")

# truncate number of microseconds (6 digits) to milliseconds (3 digits)
pdf['TS'] = pdf['TS'].str[:-3]

# Check printed timestamp and write to csv to check as well, in both cases it should follow the stand format: 2017-08-22 13:25:28.875
pdf.to_csv("C:\\Users\cmolina\\Desktop\\_MyFiles\\_SORBA files\\Task #1\\test_dsXXX.csv", sep=',', encoding='utf-8',
           index=False)

# ==============================================================


# get local now datetime with timezone
time0_local = datetime.now()  # .astimezone()
print('time0_local: ', time0_local)
print(time0_local.tzname())
print(time0_local.tzinfo)
