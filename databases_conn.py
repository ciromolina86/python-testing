
from influxdb import DataFrameClient
import json
import time
import numpy as np
import mysql.connector

import boto3
import logging
from botocore.exceptions import ClientError
from boto3.s3.transfer import TransferConfig



# ******************* Databases config class *******************************
class Config:
    # define database configuration parameters
    mysql = {}
    mysql.update({'host': "127.0.0.1"})
    mysql.update({'port': 3306})
    mysql.update({'user': "root"})
    mysql.update({'password': "sbrQp10"})
    mysql.update({'database': "config"})
    influx = {'host': "127.0.0.1", 'port': 8086, 'username': "", 'password': "", 'database': "sorba_sde"}
    amazons3 = {}
    amazons3.update({'aws_access_key_id': 'YOUR_ACCESS_KEY'})
    amazons3.update({'aws_secret_access_key': 'YOUR_SECRET_KEY'})
    amazons3.update({'region': 'us-east-1'})


# ******************* SDE Vibration Model class *******************************
class VibModel:

    # define database connection
    def __init__(self):
        self._model_mysql = self.get_model_mysql()
        self._model_influx = self.get_model_influx()

    @property
    def model_mysql(self):
        return self._model_mysql

    @property
    def model_influx(self):
        return self._model_influx

    # get the list of assets for vibration assets
    def get_asset_list(self, conn):
        """

        :param conn:
        :return: an asset list like this: ['asset1', 'asset2', ...]
        """

        # initialize assets list
        asset_list = []

        # define sql query to get all the vibration assets
        sql = 'SELECT processName ' \
              'FROM config.rt_process ' \
              'WHERE rt_process.processName LIKE "VIB_%"' \
              'ORDER BY rt_process.processName ASC'

        # query the database
        assets = conn.query(sql)

        # create the asset list
        for asset, in assets:
            # append assets to the list
            asset_list.append(asset)

        # return asset list
        return asset_list

    # get the list of groups for an asset
    @staticmethod
    def get_group_list(asset, conn):
        """

        :param asset:
        :param conn:
        :return: an asset dictionary like this: ['group1', 'group2', ...]
        """

        # initialize groups list
        group_list = []

        # define sql query to get all the groups from an asset
        sql = 'SELECT groupName ' \
              'FROM config.rt_groups ' \
              'INNER JOIN config.rt_process ON rt_groups.processID = rt_process.processID ' \
              'WHERE rt_process.processName = "{}"' \
              'ORDER BY rt_groups.groupName ASC'.format(asset)

        # query the database
        groups = conn.query(sql)

        # create the group list
        for group, in groups:
            # append groups to the list
            group_list.append(group)

        # return a group list for an asset
        return group_list

    # get the list of tags for an group
    def get_tag_list(self, asset, group, conn):
        """

        :param asset:
        :param group:
        :param conn:
        :return: a tag list like this: ['tag1', 'tag2', ...]
        """

        # initialize tags list
        tag_list = []

        # define sql query to get all the tags from a group
        sql = 'SELECT tagName ' \
              'FROM config.rt_tags_dic ' \
              'INNER JOIN config.rt_groups ON config.rt_tags_dic.groupID = config.rt_groups.groupID ' \
              'INNER JOIN config.rt_process ON config.rt_groups.processID = config.rt_process.processID ' \
              'WHERE config.rt_process.processName = "{}"' \
              'AND config.rt_groups.groupName = "{}"'.format(asset, group)

        # query the database
        tags = conn.query(sql)

        # create the tag list
        for tag, in tags:
            # append tags to the list
            tag_list.append(tag)

        # return a tag list for an group
        return tag_list

    def get_tag_id_list(self, asset, group, conn):
        """

        :param asset:
        :param group:
        :param conn:
        :return: a tag, id list like this: [(tag1, id1), (tag2, id2), ...]
        """

        # initialize (tag,id) tuple list
        tag_id_list = []

        # define sql query to get all the tags from a group
        sql = 'SELECT tagName, internalTagID ' \
              'FROM config.rt_tags_dic ' \
              'INNER JOIN config.rt_groups ON config.rt_tags_dic.groupID = config.rt_groups.groupID ' \
              'INNER JOIN config.rt_process ON config.rt_groups.processID = config.rt_process.processID ' \
              'WHERE config.rt_process.processName = "{}"' \
              'AND config.rt_groups.groupName = "{}"'.format(asset, group)

        # query the database
        tag_ids = conn.query(sql)

        for _tag, _id in tag_ids:
            # append (tag,id) tuples to the list
            tag_id_list.append((_tag, _id))

        # return a dictionary with tag: internalTagID pairs
        return tag_id_list

    # get the vibration assets model for mysql
    def get_model_mysql(self):
        """

        :return: a dictionary like this: {'asset1': {'group1: {'tag1': {'internalTagID': 519}, ...}}}
        """

        # initialize model dictionary
        model_dic = {}
        # initialize the database connection
        mysql_conn = DBmysql(info=Config.mysql)

        # format the model into a dictionary of dictionaries
        for asset in self.get_asset_list(mysql_conn):
            # update model with assets
            model_dic.update({asset: {}})

            for group in self.get_group_list(asset, mysql_conn):
                # update assets with groups
                model_dic[asset].update({group: {}})

                for _tag, _id in self.get_tag_id_list(asset, group, mysql_conn):
                    # update group with tags
                    model_dic[asset][group].update({_tag: {}})
                    # update tags with internalTagID
                    model_dic[asset][group][_tag].update({'internalTagID': _id})

        # Close database connection
        mysql_conn.exit()

        # return the complete assets dictionary
        return model_dic

    # get the vibration assets model for influx
    def get_model_influx(self):
        """

        :return:  dictionary like this: {'asset1': ['group1___tag1', 'group1___tag2', ...]}
        """

        # initialize model dictionary
        model_dic = {}
        # initialize the database connection
        mysql_conn = DBmysql(info=Config.mysql)

        # format the model into a dictionary of dictionaries
        for asset in self.get_asset_list(mysql_conn):
            # initialize columns list
            cols = []

            for group in self.get_group_list(asset, mysql_conn):

                for _tag in self.get_tag_list(asset, group, mysql_conn):
                    # append a column for each tag in a group.
                    cols.append(group + '___' + _tag)

            # update dictionary with columns list for each asset
            model_dic.update({asset: cols})

        # Close database connection
        mysql_conn.exit()

        # return the complete assets dictionary
        return model_dic

    def update_model(self):
        self._model_mysql = self.get_model_mysql()
        self._model_influx = self.get_model_influx()


# ******************* MySQL Database class *******************************
class DBmysql:

    def __init__(self, info):
        self._conn = mysql.connector.connect(**info)
        self._cursor = self._conn.cursor()
        # print('MySQL object was created')

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self.connection.commit()

    def execute(self, sql):
        self.cursor.execute(sql)

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def query(self, sql):
        self.cursor.execute(sql)
        return self.fetchall()

    def exit(self):
        self.cursor.close()
        self.connection.close()

    def get_vib_asset_list(self):
        """

        :return:
        """

        # print('get_vib_asset_list was executed')

        # define empty list for assets
        asset_list = []

        # define sql query to get all the vibration assets
        sql = 'SELECT processName FROM config.rt_process WHERE rt_process.processName LIKE "VIB_%" ORDER BY rt_process.processName ASC'

        # query the database
        assets = self.query(sql)
        print(assets)

        # create the asset list
        for asset, in assets:
            asset_list.append(asset)

        # return asset list
        return asset_list

    def get_vib_asset_dic(self):
        """

        :return: an asset dictionary like this: {'asset1': ['group1___tag1', 'group2___tag1', ...]}
        """

        # print('get_vib_asset_dic was executed')

        # define empty list for assets
        asset_dic = {}

        # get the asset list
        assets = self.get_vib_asset_list()

        for asset in assets:
            # define sql query to get all the groups and tags from vibration assets
            sql = 'SELECT groupName, tagName ' \
                   'FROM config.rt_tags_dic ' \
                   'INNER JOIN config.rt_groups ON rt_tags_dic.groupID = rt_groups.groupID ' \
                   'INNER JOIN config.rt_process ON rt_groups.processID = rt_process.processID ' \
                   'WHERE rt_process.processName = "{}"'.format(asset)

            # query the database
            groups_tags = self.query(sql)

            # define empty list
            group___tag = []

            # create the asset dictionary
            for group, tag in groups_tags:
                group___tag.append(group + '___' + tag)
                asset_dic.update({asset: group___tag})

        # return the asset dictionary
        return asset_dic

    def get_vib_tags_id_dic(self):
        """

        :return: a tag:id dictionary like this: {'asset': ['group1___tag1': internalTagID1, ...]}
        """

        # define empty dictionary for tags
        tag_id_dic = {}

        # get the asset list
        assets = self.get_vib_asset_list()

        for asset in assets:
            # define sql query to get all the groups and tags from vibration assets
            sql = 'SELECT groupName, tagName, internalTagID ' \
                  'FROM config.rt_tags_dic ' \
                  'INNER JOIN config.rt_groups ON rt_tags_dic.groupID = rt_groups.groupID ' \
                  'INNER JOIN config.rt_process ON rt_groups.processID = rt_process.processID ' \
                  'WHERE rt_process.processName = "{}"'.format(asset)

            # query the database
            groups_tags = self.query(sql)

            # define empty list
            group___tag = []

            # create the asset dictionary
            for group, tag, internalTagID in groups_tags:
                group___tag.append((group + '___' + tag, internalTagID))
                tag_id_dic.update({asset: group___tag})

        # return the tags dictionary
        return tag_id_dic


# ******************* Influx Database class *******************************
class DBinflux:

    def __init__(self, config):
        self._client = DataFrameClient(**config)

    @property
    def client(self):
        return self._client

    def query(self, sql, bind_params={}):
        return self.client.query(query=sql, bind_params=bind_params)

    def write_points(self, pdf, meas, tag_columns):
        if tag_columns is None:
            self.client.write_points(dataframe=pdf, measurement=meas, time_precision='ms')
        else:
            self.client.write_points(dataframe=pdf, measurement=meas, time_precision='ms', tag_columns=tag_columns)


# ******************* getinrtmatrix Function *******************************
def getinrtmatrix(rt_redis_data, in_tags_str):
    # Local Initialization
    intagsstr_redis_list = []
    input_tags_values = []
    input_tags_timestamp = []
    redis_retry = True
    redis_retry_counter = 0

    # Convert Input Tags strings to List
    internaltagidlist = list(filter(lambda e: e != '', in_tags_str.split(",")))

    # Get Tags Amount
    n = len(internaltagidlist)

    # Create a Tags IDs List to be use with Redis
    for i in range(n):
        intagsstr_redis_list.append("rt_data:" + str(internaltagidlist[i]))

    while (redis_retry is True) and (redis_retry_counter <= 10):
        # Get List of Values from Redis
        redis_info_list = rt_redis_data.get_value_list(intagsstr_redis_list)

        # Create the Input Tags List with Values and Timestamp
        for k in range(n):
            if redis_info_list[k] is not None:
                redis_info_temp = json.loads(redis_info_list[k])
                input_tags_values.append(float(redis_info_temp["value"]))
                input_tags_timestamp.append(redis_info_temp["timestamp"])
                redis_retry = False
            else:
                # Disconnect from Redis DB
                rt_redis_data.close_db()

                # Sleep to create Scan Cycle = Configuration Loop Frequency
                time.sleep(0.1)

                # Connect to Redis DB
                rt_redis_data.open_db()
                redis_retry = True
                redis_retry_counter += 1
                print("{Warning} Real Time DB is empty")

    # Get the Latest Timestamp Value for the Tags
    if not input_tags_timestamp:
        input_timestamp = None
        input_tags_values = None
    else:
        input_timestamp = max(input_tags_timestamp)
        input_tags_values = np.asarray(input_tags_values)

    return input_timestamp, input_tags_values


# ******************* redis_get_value Function *******************************
def redis_get_value(rt_redis_data, redis_key):
    """

    :param rt_redis_data:
    :param redis_key:
    :return:
    """

    # Initialization
    redis_retry = True
    redis_value = None
    redis_retry_counter = 0
    max_retry = 30

    while (redis_retry is True) and (redis_retry_counter <= max_retry):
        # Get Value from Redis
        redis_value = rt_redis_data.get_value(redis_key)

        if redis_value is not None:
            redis_retry = False
        else:
            # Disconnect from Redis DB
            rt_redis_data.close_db()

            # Sleep to create Scan Cycle = Configuration Loop Frequency
            time.sleep(0.1)

            # Connect to Redis DB
            rt_redis_data.open_db()
            redis_retry = True
            redis_retry_counter += 1

    return redis_value
    pass


# ******************* redis_set_value Function *******************************
def redis_set_value(rt_redis_data, redis_key, redis_value):
    """

    :param rt_redis_data:
    :param redis_key:
    :param redis_value:
    :return:
    """

    # Initialization
    redis_retry = True
    redis_retry_counter = 0
    max_retry = 30

    while (redis_retry is True) and (redis_retry_counter <= max_retry):
        # noinspection PyBroadException
        try:
            # Set Value to Redis
            rt_redis_data.set_value(redis_key, redis_value)
            redis_retry = False
        except Exception:
            # Disconnect from Redis DB
            rt_redis_data.close_db()

            # Sleep to create Scan Cycle = Configuration Loop Frequency
            time.sleep(0.1)

            # Connect to Redis DB
            rt_redis_data.open_db()
            redis_retry = True
            redis_retry_counter += 1

    pass

# ******************* Amazon S3 Database class *******************************
class DBamazons3:

    def __init__(self):
        self._client = boto3.client('s3')   #boto3.resource('s3')

    @property
    def client(self):
        return self._client

    def download_file(self, bucket_name, key, file_name, extra_args=None, call_back=None, config=None):
        """Download a file to an S3 bucket

                :param file_name: The path to the file to download to
                :param bucket_name: The name of the bucket to download from.
                :param key: The name of the key (object) to download from

                :return: True if file was downloaded, else False
                """

        try:
            response = self.client.download_file(Bucket=bucket_name, Key=key, Filename=file_name, ExtraArgs=None, Callback=None, Config=None)
            logging.info('[INFO] S3 file downloaded successfully s3://{}/{}'.format(bucket_name, key))
            # print(response)

        except ClientError as e:
            # print('[ERROR] Failed to download s3 file s3://{}/{}'.format(bucket_name, key))
            # print('[ERROR]', e)
            raise e


    def upload_file(self, bucket_name, key, file_name):
        """Upload a file to an S3 bucket

        :param file_name: File to upload
        :param bucket_name: Bucket to upload to
        :param key: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """

        try:
            response = self.client.upload_file(Bucket=bucket_name, Key=key, Filename=file_name, ExtraArgs={'ACL':'bucket-owner-full-control'}, Callback=None, Config=None)
            logging.info('[INFO] S3 file uploaded successfully s3://{}/{}'.format(bucket_name, key))
            # print(response)

        except ClientError as e:
            # print('[ERROR] Failed to upload s3 file s3://{}/{}'.format(bucket_name, key))
            # print('[ERROR]', e)
            raise e
            

    def get_s3_keys(self, bucket_name):
        """Get a list of keys in an S3 bucket."""
        key_list = []
        resp = self.client.list_objects_v2(Bucket=bucket_name)
        for obj in resp['Contents']:
            key_list.append(obj['Key'])
        return key_list

    def get_all_s3_keys(self, bucket_name):
        """Get a list of all keys in an S3 bucket."""
        key_list = []

        kwargs = {'Bucket': bucket_name}
        while True:
            # The S3 API response is a large blob of metadata.
            # 'Contents' contains information about the listed objects.
            resp = self.client.list_objects_v2(**kwargs)
            for obj in resp['Contents']:
                key_list.append(obj['Key'])

            try:
                # The S3 API is paginated, returning up to 1000 keys at a time.
                # Pass the continuation token into the next response, until we
                # reach the final page (when this field is missing).
                kwargs['ContinuationToken'] = resp['NextContinuationToken']
            except KeyError:
                break

        return key_list

    def get_matching_s3_keys(self, bucket_name, prefix='', suffix=''):
        """
        Generate the keys in an S3 bucket.

        :param bucket_name: Name of the S3 bucket.
        :param prefix: Only fetch keys that start with this prefix (optional).
        :param suffix: Only fetch keys that end with this suffix (optional).
        """

        kwargs = {'Bucket': bucket_name}

        # If the prefix is a single string (not a tuple of strings), we can
        # do the filtering directly in the S3 API.
        if isinstance(prefix, str):
            kwargs['Prefix'] = prefix

        while True:

            # The S3 API response is a large blob of metadata.
            # 'Contents' contains information about the listed objects.
            resp = self.client.list_objects_v2(**kwargs)
            for obj in resp['Contents']:
                key = obj['Key']
                if key.startswith(prefix) and key.endswith(suffix):
                    yield key

            # The S3 API is paginated, returning up to 1000 keys at a time.
            # Pass the continuation token into the next response, until we
            # reach the final page (when this field is missing).
            try:
                kwargs['ContinuationToken'] = resp['NextContinuationToken']
            except KeyError:
                break

    '''def s3_ls(self, bucket, prefix):
        # ls [prefix]

        paginator = self.client.get_paginator('list_objects')
        result = paginator.paginate(Bucket=bucket, Prefix=prefix, Delimiter='/')
        files = [common_prefix.get('Prefix')
                 for common_prefix in result.search('CommonPrefixes')]
    
        return files

    def s3_ls_r(self, bucket, prefix):
        # ls -R [prefix]

        bucket = self.client.Bucket(bucket)
        files = [x.key for x in bucket.objects.filter(Prefix=prefix)]

        return files'''
