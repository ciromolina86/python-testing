import pandas as pd
import datetime
from datetime import datetime
import time
import multiprocessing as mp
from functools import partial
import test_os
import re


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


def check_data_consistency(file_name: str):
    # print file name being processed
    print(file_name)

    # read csv into a dataframe
    file_name = pd.read_csv(file_name)

    # fill empty values forward and backward
    file_name.fillna(method='ffill', inplace=True)
    file_name.fillna(method='bfill', inplace=True)

    # write dataframe to csv
    file_name.to_csv(file_name)

# do not use this !!! kept just for reference
def fmt_narrow_to_wide_s7_hmi_to_sdc(file_name: str, dst_dir_name: str):
    '''
    implemented by using brute force (very inefficient)

    :param file_name:
    :param dst_dir_name:
    :return:
    '''
    # print file name being processed
    print(file_name)

    # read csv into a dataframe
    df_src = pd.read_csv(file_name, delimiter=';', skipfooter=1, engine='python')

    # create the result empty dataframe
    df_dst = pd.DataFrame()

    for time_str in list(df_src['TimeString'].unique())[:]:
        # get current time
        start_ts1 = time.time()

        # convert source time format to desired time format
        # source: 07.11.2019 19:23:35
        _time = datetime.strptime(time_str, "%d.%m.%Y %H:%M:%S")
        # destination: 11/07/2019 19:23:35
        _time = _time.strftime("%m/%d/%Y %H:%M:%S")

        # debug print
        # print datetime being processed
        print('{}/{} >>> gathering data for: {}'.format(list(df_src['TimeString'].unique()).index(time_str),
                                                        len(list(df_src['TimeString'].unique())), _time))

        # temporary dataframe to be appended to result wide format dataframe
        df_tmp = pd.DataFrame({'Time': [_time]})

        # debug
        # init tag counter
        # i = 0
        for _, row in df_src.iterrows():
            if time_str == row.TimeString:
                # debug print
                # count how many tags are logged for each timestamp
                # i += 1
                # print(row)
                # print(i)
                # print(row.TimeString)

                if row.Validity == 1:
                    # cast the string to float and create a new column with its value
                    df_tmp[row.VarName] = float(row.VarValue.replace(',', '.'))

        # debug print
        # print(df_tmp.head())

        # append the temp dataframe  to the result dataframe (wide format)
        df_dst = df_dst.append(df_tmp, ignore_index=True)

        # get current time
        end_ts1 = time.time()
        # print time delta to see how long the processing takes in seconds
        print('time: {}s sec'.format(end_ts1 - start_ts1))

        # write dataframe to csv file every time all data for certain datetime is found
        # this way it allows to see the progress on the wide .csv file
        df_dst.to_csv(dst_dir_name + file_name.split('\\')[-1])

# use this !!!
def fmt_narrow_to_wide_s7_hmi_to_sdc2(file_name: str, dst_dir_name: str):
    '''
    this function reformats narrow-formatted data that come from Siemens HMI logs
    into wide-formatted data compatible with SDE Simulation channel

    implemented by using pandas dataframe pivot function (very efficient)

    :param file_name:
    :param dst_dir_name:
    :return:
    '''

    # get current time
    start_ts1 = time.time()

    # print file name being processed
    print(file_name)

    # read csv into a dataframe
    df_src = pd.read_csv(file_name, delimiter=';', skipfooter=1, engine='python')

    # check consistency
    df_src.dropna(axis=0, inplace=True)
    df_src = df_src[df_src['Validity'] > 0]
    df_src['TimeString'] = df_src['TimeString'].map(lambda x: check_dt_consistency(x))

    # create the result empty dataframe
    df_dst = pd.DataFrame()

    # convert source time format to desired time format
    # source: 07.11.2019 19:23:35
    # destination: 11/07/2019 19:23:35
    df_src['TimeString'] = pd.to_datetime(df_src['TimeString'],
                                          format='%d.%m.%Y %H:%M:%S')  # infer_datetime_format=True
    df_src['TimeString'] = df_src['TimeString'].dt.strftime('%m/%d/%Y %H:%M:%S')

    # rename time column name
    df_src.rename({'TimeString': 'Time'}, axis='columns', inplace=True)

    # cast value column to float
    df_src['VarValue'] = df_src['VarValue'].map(lambda x: float(x.replace(',', '.')))

    # debug print
    # print(len(list(df_src['Time'].unique())))
    # print(df_src.shape)

    # create the result empty dataframe
    df_dst = df_src.pivot_table(index='Time', columns='VarName', values='VarValue')

    # remove $RT_OFF$ column if exists
    if '$RT_OFF$' in df_dst.columns:
        df_dst.drop(columns=['$RT_OFF$'], inplace=True)

    # check dataframe consistency
    df_dst.fillna(method='ffill', inplace=True)
    df_dst.fillna(method='bfill', inplace=True)

    # get current time
    end_ts1 = time.time()
    # print time delta to see how long the processing takes in seconds
    print('time: {}s sec'.format(end_ts1 - start_ts1))

    # write dataframe to csv file every time all data for certain datetime is found
    # this way it allows to see the progress on the wide .csv file
    df_dst.to_csv(dst_dir_name + file_name.split('\\')[-1])

    # print(df_dst)


def merge_files(files: list, dst_dir_name: str):
    # create the result empty dataframe
    df_dst = pd.DataFrame()

    # get current time
    start_ts1 = time.time()

    for file in files:
        # print file name being processed
        print(file)

        # read csv into a dataframe
        df_tmp = pd.read_csv(file).set_index('Time')

        print(df_tmp.index[0])

        df_dst = pd.concat([df_dst, df_tmp])
        df_dst = df_dst.sort_index()

        print(df_dst.shape)

    # write dataframe to csv file every time all data for certain datetime is found
    # this way it allows to see the progress on the wide .csv file
    df_dst.to_csv(dst_dir_name + 'merged_data.csv')

    # get current time
    end_ts1 = time.time()
    # print time delta to see how long the processing takes in seconds
    print('time: {}s sec'.format(end_ts1 - start_ts1))


def main():
    src_dir_name = 'C:\\Users\\cmolina\\Downloads\\S7 HMI  Logs\\Narrow files\\'
    dst_dir_name = 'C:\\Users\\cmolina\\Downloads\\S7 HMI  Logs\\Wide files\\'

    file_names = test_os.get_local_files_names(src_dir_name)[:]

    # method 1
    # for file_name in file_names:
    #     fmt_narrow_to_wide_s7_hmi_to_sdc2(file_name, dst_dir_name)

    # method 2
    with mp.Pool(processes=4, maxtasksperchild=1) as pool:
        pool.map_async(partial(fmt_narrow_to_wide_s7_hmi_to_sdc2, dst_dir_name=dst_dir_name), file_names,
                       chunksize=1).get()
        pool.close()
        pool.join()

    # get files list to be merged
    file_names = test_os.get_local_files_names(dst_dir_name)[:]

    # merge all wide files into a single file (e.g.: merged_data.csv)
    merge_files(file_names, dst_dir_name)


if __name__ == '__main__':
    main()

    '''
    # merge all the merged_data.csv files from different processing lots
    dst_dir_name = 'C:\\Users\\cmolina\\Downloads\\S7 HMI  Logs\\Wide files\\'
    file_names = test_os.get_local_files_names(dst_dir_name)[:]
    merge_files(file_names, dst_dir_name)
    '''
