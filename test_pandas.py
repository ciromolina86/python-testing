import pandas as pd
import math

# records = [{'name':f'asset1.group1.tag{x}', 'time':1618350233000+x, 'value':float(x*x)} for x in range(3)]
# records += [{'name':f'asset2.group1.tag{x}', 'time':1618350233000+x, 'value':float(x*x)} for x in range(3)]

records = [
    {'name': 'asset1.group1.tag1', 'time': [1618350233000 + x for x in range(20000)], 'value': [x for x in range(20000)]},
    {'name': 'asset2.group1.tag2', 'time': [1618350233000 + x for x in range(20000)], 'value': [x for x in range(20000)]},
    {'name': 'asset3.group1.tag3', 'time': [1618350233000 + x for x in range(20000)], 'value': [x for x in range(20000)]}
]
'''
for obj in records:
    # create dataframe
    df = pd.DataFrame(obj)
    # print(df)

    # extract asset from tag name and insert it in ne column
    df['asset'] = df['name'].map(lambda x: x.split('.')[0])
    # print(df)

    # rename fields with certain format
    df['name'] = df['name'].map(lambda x: '___'.join([x.split('.')[1], x.split('.')[2]]))
    # print(df)
    # print(df['asset'][0])

    # extract dataframe to be pivoted
    df = df.set_index('asset').loc[df['asset'][0]]
    # print(df)

    # pivot dataframe to desired format (wide)
    df = df.pivot_table(index='time', columns='name', values='value')
    # print(df)

    # unpack dataframe shape
    rows, cols = df.shape

    # compute batch count
    batch_count = math.ceil(rows/1000)

    # print dataframe slices (e.g. df[from_index:to_index])
    for batch in range(batch_count):
        print(df[1000*batch:1000*(batch+1)])
'''

