import pandas as pd
import json


def main():
    data = {}

    df = pd.read_csv('tags_Target.csv')
    plcs = df.iloc[:, 3].unique()

    for plc in plcs:
        data.update({plc: {}})

    for i in df.index:
        data[f'{df.iloc[i, 3]}'].update({f'{df.iloc[i, 0]}.{df.iloc[i, 1]}.{df.iloc[i, 2]}': f'{df.iloc[i, 4]}'})

    # write file list to a json file
    with open('script-engine-tags.json', 'w') as f:
        json_string = json.dumps(data, indent=4)
        f.write(json_string)


if __name__ == '__main__':
    main()
