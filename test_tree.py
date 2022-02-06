def print_tree(dic, level_no=0, level=''):
    '''
    creating a tree from a dic in console

    :param dic:
    :param level_no:
    :return:
    '''

    if type(dic) == dict:
        for key in dic:
            if type(dic[key]) == dict:
                # print('{}: {}{}'.format(level_no, level, key))
                print('{}{}'.format(level, key))
                print_tree(dic[key], level_no+1, '|   '*level_no+'|---+ ')
            else:
                print('{}{}'.format(level[:-2]+' ', key))


def get_paths(dic, level_no=0, path=''):
    '''
    get a list of paths from a dictionary separated by dots
    e.g. key1_level1.key1_level2.key1_level3

    :param dic:
    :param level_no:
    :param path:
    :return:
    '''
    paths = []
    level_no += 1

    if type(dic) == dict:
        for key in dic:
            # print('level:',level_no)
            # print('key:',key)
            path = '.'.join(path.split('.')[:level_no])
            path = '.'.join([path, key])
            # print('path: ',path)

            if type(dic[key]) == dict:
                paths = paths + get_paths(dic[key], level_no, path)
            else:
                paths.append(path[1:])
                # print('paths:',paths)

    return paths


if __name__ == '__main__':
    import json

    dic = {}
    dic.update({'key1_level1': {}})
    dic['key1_level1'].update({'value2_level2':10})
    dic['key1_level1'].update({'key1_level2': {}})
    dic['key1_level1']['key1_level2'].update({'value1_level1': 10})
    dic['key1_level1'].update({'key2_level2': {}})
    dic['key1_level1']['key2_level2'].update({'key1_level3': {}})
    dic['key1_level1']['key2_level2']['key1_level3'].update({'value3_level4': 10})

    dic['key1_level1'].update({'key3_level2':{}})
    dic['key1_level1']['key3_level2'].update({'value4_level3':10})
    # dic['key1_level1'].update({'value5_level2':10})
    dic['key1_level1'].update({'key4_level2':{}})
    dic['key1_level1']['key4_level2'].update({'key1_level3':{}})
    dic['key1_level1']['key4_level2']['key1_level3'].update({'value6_level4':10})

    print(json.dumps(dic, indent=4))
    print('\n')

    print_tree(dic)
    print('\n')

    # paths = get_paths(dic)
    # for path in paths:
    #     print(path)
