from multiprocessing import Pool, Lock, cpu_count, Process
from functools import partial

import json
import os
import time

# import databases_conn

mutex = Lock()

def check_for_new_file(json_file_name, file_name):
    # mutex.acquire()
    # try:

    time.sleep(1)

    # Check if temp file exist
    if os.path.isfile(json_file_name):

        try:
            # read log file
            with open(json_file_name) as json_file_tmp:
                logs = json.load(json_file_tmp)

            # check if the file has been downloaded, fft processed and uploaded,
            # otherwise, begin from the beginning
            if file_name not in logs['download_file_list'] or \
                    file_name not in logs['fft_file_list'] or \
                    file_name not in logs['upload_file_list']:
                return True

            else:
                return False

        except Exception:
            # Create logs dictionary
            logs = {'download_file_list': [], 'fft_file_list': [], 'upload_file_list': [], 'error_file_list': []}

            # Write logs json file
            with open(json_file_name, 'w') as json_file_tmp:
                json.dump(logs, json_file_tmp)

            return True

    else:
        # Create logs dictionary
        logs = {'download_file_list': [], 'fft_file_list': [], 'upload_file_list': [], 'error_file_list': []}

        # Write logs json file
        with open(json_file_name, 'w') as json_file_tmp:
            json.dump(logs, json_file_tmp)

        return True

    # finally:
    #     mutex.release()
    # db1 = import databases_conn.



def update_download_logs(json_file_name, file_name, ts=''):
    # mutex.acquire()
    # try:
    time.sleep(0.1)
    # read log file
    with open(json_file_name) as f:
        logs = json.load(f)

    # update log file
    # if file_name in logs['download_file_list']:
    #     logs['download_file_list'].remove(file_name)

    logs['download_file_list'].append(file_name)
    # logs[file_name] = {}
    # logs[file_name].update({'download_ts': ts})

    # write updated log file
    with open(json_file_name, 'w') as f:
        json.dump(logs, f, indent=4)

    # finally:
    #     mutex.release()


def calc_square(i):
    time.sleep(1)
    print('square: ', str(i * i))


def processData(data):
    json_file = 'C:\\Users\\cmolina\\PycharmProjects\\my-scripts\\sample.json'

    print('>>>>>>>', os.getpid())

    res = check_for_new_file(json_file, data)
    if res:
        update_download_logs(json_file, data)


if __name__ == '__main__':

    file_names = list(range(100))
    print(file_names)
    print(cpu_count())

    start = time.time()

    with Pool(processes=cpu_count(), maxtasksperchild=1) as pool:
        pool.map(processData, file_names, chunksize=1)
        # pool.map(calc_square, file_names, chunksize=1)
        pool.close()
        pool.join()

    # for num in range(1000):
    #     Process(target=processData, args=(mutex, num)).start()


    # for i in file_names:
        # processData(mutex,i)
        # calc_square(i)

    end = time.time()
    print(end-start)
