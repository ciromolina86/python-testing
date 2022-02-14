import os


def get_local_files_names(dir_name):
    '''

    :param dir_name:
    :return:
    '''

    completeFileList = []

    for file in os.listdir(dir_name):
        completePath = os.path.join(dir_name, file)

        if os.path.isdir(completePath):
            completeFileList = completeFileList + get_local_files_names(completePath)
        else:
            completeFileList.append(completePath)

    return completeFileList


def remove_empty_dir(root_dir):
    try:
        for dir_path, dir_names, file_names in os.walk(root_dir, topdown=False):
            print(f'dir_path={dir_path}')
            print(f'dir_names={dir_names}')
            print(f'file_names={file_names}')

            for file in file_names:
                os.unlink(os.path.join(dir_path, file))

        for dir_path, dir_names, file_names in os.walk(root_dir, topdown=False):
            print(f'dir_path={dir_path}')
            print(f'dir_names={dir_names}')
            print(f'file_names={file_names}')

            if dir_path != root_dir and len(os.listdir(dir_path)) == 0:
                os.rmdir(dir_path)
    except Exception as e:
        print('[ERROR] Failed to remove empty folders')
        print('[ERROR] {}'.format(type(e)))
        print('[ERROR] {}'.format(e))


if __name__ == '__main__':
    remove_empty_dir('D:/OneDrive - ITG Technologies/Documents/ITG Clients/')
