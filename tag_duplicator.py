import pandas as pd
import json
import os


def read_data_setting_json(path: os.path):
    # read json file
    with open(path, 'r') as f:
        data = json.load(f)
    return data


def write_data_setting_json(path: os.path, data: dict):
    # write json file
    with open(path, 'w') as f:
        json_string = json.dumps(data, indent=4)
        f.write(json_string)


def read_data_setting_csv(path: os.path):
    # read csv file
    data = pd.read_csv(path)
    rows, cols = data.shape
    # print(data)

    return data


def duplicate_asset(data: pd.DataFrame, assets) -> pd.DataFrame:
    """

    :param data: sample asset dataframe
    :return: resulting dataframe with all assets
    """

    data_result = pd.DataFrame()

    for asset in assets:
        data['Asset name'] = asset
        data_result = data_result.append(data)

    return data_result


def test_data_setting_json():
    data = read_data_setting_json('data_settings_backup-6_14_2021-14_20_13.json')

    for asset in data['assets']:
        print(asset['processName'])

    for group in data['groups']:
        print(group['groupName'])

    for tag in data['tags']:
        print(tag['tagName'])


def test_data_setting_csv():
    tag_setting = read_data_setting_csv('data_settings_backup-6_14_2021-14_31_33.txt')
    print(tag_setting)

    tag_setting = duplicate_asset(tag_setting, assets=['asset1', 'asset2', 'asset3'])
    print(tag_setting)


def main():
    _type = {
        'groups':
            [
                {
                    'name': 'group1',
                    'tags':
                        [
                            {
                                'name': 'tag11',
                                'desc': 'desc11',
                                'dtype': 'Real'
                            },
                            {
                                'name': 'tag12',
                                'desc': 'desc12',
                                'dtype': 'Real'
                            }
                        ]
                },
                {
                    'name': 'group2',
                    'tags':
                        [
                            {
                                'name': 'tag21',
                                'desc': 'desc21',
                                'dtype': 'Real'
                            },
                            {
                                'name': 'tag22',
                                'desc': 'desc22',
                                'dtype': 'Real'
                            }
                        ]
                }
            ]
    }
    _assets = ['asset1', 'asset2', 'asset3']

    for asset in _assets:
        print(asset)
        for group_obj in _type['groups']:
            print('\t', group_obj['name'])
            for tag_obj in group_obj['tags']:
                print('\t\t', tag_obj['name'])


if __name__ == '__main__':
    # main()
    # test_data_setting_json()
    test_data_setting_csv()
