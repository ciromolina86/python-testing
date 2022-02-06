'''
===================================================================
==================== AWS S3 VOLTA FILES ===========================
===================================================================
'''


import re
import pandas as pd
import numpy as np
import pyarrow.parquet as pq
import datetime
import sys
import boto3


def get_sensor_id(filename):
    regex = re.compile(r'.*Node_([0-9]+)_[0-9]+_[0-9]+_[0-9]+(.*?)\.esa')
    result = regex.match(filename)
    matches = result.groups()
    if matches is None:
        print(
            "Error: _get_start_time: file name not matching the pattern:", filename)
    return matches[0]


def get_start_timestamp(filename):
    regex = re.compile(r'.*Node_[0-9]+_[0-9]+_[0-9]+_([0-9]+)(.*?)\.esa')
    result = regex.match(filename)
    matches = result.groups()
    if matches is None:
        print(
            "Error: _get_start_time: file name not matching the pattern:", filename)
    epoch = int(matches[0]) * 1000000000
    start = np.datetime64(epoch, 'ns')

    return start


def parse_file(s3_param, filename):

    try:
        # skip extra comma in the header
        usecols = ['time (sec)', ' Va', ' Ia', ' Vb', ' Ib', ' Vc', ' Ic']
        df_data = pd.read_csv(filename, usecols=usecols)

        # remove space in front of column name
        df_data.columns = ['time (sec)', 'Va', 'Ia', 'Vb', 'Ib', 'Vc', 'Ic']

        # add sensor_id and event_id
        df_data['sensor_id'] = [get_sensor_id(filename)] * len(df_data)

        # parse timestamp
        start = get_start_timestamp(filename)

        # add the event_id columns to data-frame
        df_data['event_id'] = start
        df_data['event_id'] = df_data['event_id'].dt.strftime("%Y-%m-%d %H:%M:%S.%f")

        # create timestamp using start + delta time
        df_data['time (sec)'] = df_data['time (sec)'].map(lambda x: start + np.timedelta64(round(x * 1000000000), 'ns'))

        # add the _ts column to data-frame
        df_data['_ts'] = df_data['time (sec)'].dt.strftime("%Y-%m-%d %H:%M:%S.%f")

        # set timestamp as index
        df_data = df_data.set_index('time (sec)')

        # remove data that is not needed
        df_data = df_data[['_ts', 'event_id']+s3_param['s3_volta_tdw_motor_report_cols']]

        # cast datatype of data columns to float
        df_data[s3_param['tdw_cols_elec']] = df_data[s3_param['tdw_cols_elec']].astype('float64')

        # calculate framerate (in hertz) from delta time (in seconds)
        framerate = 1/(df_data.index[1]-df_data.index[0]).total_seconds()
        # print('[INFO] Frame Rate (Fs) in Hz : {}'.format(framerate))

        return framerate, df_data

    except Exception as e:
        # print('[ERROR]', e)
        raise e
