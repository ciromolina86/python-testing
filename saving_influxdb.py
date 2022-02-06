from time import time
import datetime
import pandas as pd
from influxdb import DataFrameClient
import math
import json

records = [
    {
        'tag_name': 'VIB_CRBTS.WF.X_TDW',
        'timestamp': [(1619101366968 + i) * 1000000 for i in range(1)],
        'values': [float(i) for i in range(1)]
    },
    {
        'tag_name': 'VIB_CRBTS.WF.X_TDW',
        'timestamp': [(1619101366968 + i) * 1000000 for i in range(1)],
        'values': [float(i) for i in range(1)]
    }

]




def retry(max_attempts: int, interval_delay_ms: int = 1000,
          raise_in_limit: bool = False, verbose: bool = False):
    """Retry a function call if it throw an error.

    If you decorate a function with @retry(n), every time you invoke it, if it
    raise an error in some part of its body, the decorator will try execute it
    again, and so on until the max_attempts was reached.

    After error the main thread will sleep for interval_delay_ms (ms) before
    the function was called again.

    If all attempts result in errors and raise_in_limit is True, then the last
    caught error will be threw as well. If raise_in_limit is False, the thread
    will continue to the next line after the function call.

    On every handled error, if verbose is True, e message log will be printed
    for the standard output.

    Despite all these parameters are set when you define the function, at
    runtime, when the function is invoked, all these parameters can be overrode
    using the next keyword arguments:
    - override_max_attempts
    - override_delay_ms
    - override_raise
    - override_verbose
    """

    def decorator(function: callable):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            iterations = max_attempts
            delay = interval_delay_ms
            raise_ = raise_in_limit
            verbose_ = verbose
            if "override_max_attempts" in kwargs:
                iterations = kwargs["override_max_attempts"]
                del kwargs["override_max_attempts"]
            if "override_delay_ms" in kwargs:
                delay = kwargs["override_delay_ms"]
                del kwargs["override_delay_ms"]
            if "override_raise" in kwargs:
                raise_ = kwargs["override_raise"]
                del kwargs["override_raise"]
            if "override_verbose" in kwargs:
                verbose_ = kwargs["override_verbose"]
                del kwargs["override_verbose"]
            for i in range(iterations):
                try:
                    return function(*args, **kwargs)
                except Exception as err:
                    if verbose_ is True:
                        log(
                            title="{}".format(function.__name__),
                            type_=LogType.ERROR,
                            message="Attempt: {}\n{}".format(i + 1, err)
                        )
                    if raise_ is True and i + 1 == iterations:
                        raise
                    time.sleep(delay / 1000)

        return wrapper

    return decorator


def get_df_client(**kwargs):
    client = DataFrameClient(
        host=kwargs["host"] if "host" in kwargs else "localhost",
        port=kwargs["port"] if "port" in kwargs else 8086,
        username=kwargs["username"] if "username" in kwargs else "root",
        password=kwargs["password"] if "password" in kwargs else "root",
        database=kwargs["database"] if "database" in kwargs else None,
        ssl=kwargs["ssl"] if "ssl" in kwargs else False,
        verify_ssl=kwargs["verify_ssl"] if "verify_ssl" in kwargs else False,
        timeout=kwargs["timeout"] if "timeout" in kwargs else None,
        retries=1,
        use_udp=kwargs["use_udp"] if "use_udp" in kwargs else False,
        udp_port=kwargs["udp_port"] if "udp_port" in kwargs else 4444,
        proxies=kwargs["proxies"] if "proxies" in kwargs else None,
        pool_size=kwargs["pool_size"] if "pool_size" in kwargs else 10,
        path=kwargs["path"] if "path" in kwargs else "",
        cert=kwargs["cert"] if "cert" in kwargs else None,
        gzip=kwargs["gzip"] if "gzip" in kwargs else False,
        session=kwargs["session"] if "session" in kwargs else None,
        headers=kwargs["headers"] if "headers" in kwargs else None
    )

    return client


# @decorators.retry(3, 100, False)
def write_df_points(**kwargs):
    """Write to multiple time series names."""
    client = get_df_client(**kwargs)
    f_args = client.write_points.__code__.co_varnames
    wp_args = {key: val for key, val in kwargs.items() if key in f_args}

    return client.write_points(**wp_args)


def saving_influxdb(_records: list, batch_limit: int = 1000):
    try:
        records = _records
        if len(records) > 0:
            for obj in records:
                if type(obj['timestamp']) is list and type(obj['values']) is list:
                    if len(obj['timestamp']) == len(obj['values']):
                        df = pd.DataFrame(obj)
                    elif len(obj['timestamp']) > len(obj['values']):
                        obj['timestamp'] = obj['timestamp'][:len(
                            obj['values'])]
                        df = pd.DataFrame(obj)
                    else:
                        obj['values'] = obj['values'][:len(obj['timestamp'])]
                        df = pd.DataFrame(obj)

                    df['asset'] = df['tag_name'].map(lambda x: x.split('.')[0])
                    df['tag_name'] = df['tag_name'].map(
                        lambda x: '___'.join(x.split('.')[1:])
                    )
                    asset = df['asset'][0]
                    df = df.set_index('asset').loc[df['asset'][0]]
                    df['timestamp'] = pd.to_datetime(
                        df['timestamp'], unit='ns'
                    )
                    df.set_index('timestamp', inplace=True)
                    df = df.pivot_table(columns='tag_name',
                                        values='values',
                                        index='timestamp'
                                        )
                    write_df_points(host='192.168.43.147',
                                    port=8086,
                                    username='sdc',
                                    password='sbrQp10',
                                    database='sorba_sde',
                                    dataframe=df,
                                    measurement=asset,
                                    time_precision='ms',
                                    batch_size=batch_limit)
                else:
                    raise TypeError(
                        'Data format invalid, expected timestamp and values as list')
            return True
    except Exception as msg:
        raise Exception(
            '[ERROR] Runtime error writing in influxdb {}'.format(msg)
        )


if __name__ == '__main__':
    ts = datetime.datetime.now().timestamp()
    with open("/home/eduardo/Descargas/Testing_FFT/records.json") as data:
        _records = json.loads(data.readlines()[0])

        
        temp = _records.copy()
        for obj in temp:
            obj["timestamp"] = []
            for pos in range(len(obj["values"])):
                obj["timestamp"].append(((ts * 1000) + pos) * 1000)
        
        
        x = saving_influxdb(temp)
        if x:
            print('Hola')
