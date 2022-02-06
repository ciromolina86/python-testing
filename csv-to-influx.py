import pandas as pd
import re
from influxdb import DataFrameClient

# ******************* Influx Database class *******************************
class DBinflux:

    def __init__(self):
        self._client = DataFrameClient(host="192.168.91.134", port=8086, username="", password="", database="sorba_sde")

    @property
    def client(self):
        return self._client

    def query(self, sql, bind_params={}):
        print('querying influxdb')
        return self.client.query(query=sql, bind_params=bind_params)

    def write_points(self, df, meas, tag_columns=None):
        print('writing points to influxdb')
        if tag_columns is None:
            self.client.write_points(dataframe=df, measurement=meas, time_precision='ms')
        else:
            self.client.write_points(dataframe=df, measurement=meas, tag_columns=tag_columns, time_precision='ms')


def check_dt_consistency(date_time: str):
    # search for a pattern match
    _match = re.search("(\d+.\d+.\d+)( \d+)?(:\d+)?(:\d+)?", date_time)
    #             GROUP:      1         2      3      4
    if _match.group(2) and _match.group(3) and _match.group(4):
        return date_time
    elif _match.group(2) and _match.group(3):
        return _match.group(1)+_match.group(2)+_match.group(3) + ":00"
    elif _match.group(2):
        return _match.group(1)+_match.group(2)+":00:00"
    else:
        return _match.group(1) + " 00:00:00"


def main():
    src_dir_name = 'C:\\Users\\cmolina\\Downloads\\S7 HMI  Logs\\'
    df = pd.read_csv(src_dir_name+'merged_data-3-influx.csv')
    df['Time'] = df['Time'].map(lambda x: check_dt_consistency(x))
    df['Time'] = pd.to_datetime(df['Time'], format='%m/%d/%Y %H:%M:%S')
    df.set_index('Time', inplace=True)

    row, col = df.shape
    db = DBinflux()

    # writing points to influx is restricted by the influxdb retention policy
    # in this case, the SDE has 7 days, so no more than 7 days are allowed to be written
    db.write_points(df, 'BPS')

    # temp = df[:int(row/4)]
    # print(temp)
    # db.write_points(temp, 'BPS')
    # temp = df[int(row/4):int(row / 4)*2]
    # db.write_points(temp, 'BPS')
    # temp = df[int(row / 4)*2:int(row / 4) * 3]
    # db.write_points(temp, 'BPS')
    # temp = df[int(row / 4) * 3:]
    # db.write_points(temp, 'BPS')


if __name__ == '__main__':
    main()
