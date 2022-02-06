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


if __name__ == '__main__':
    
    files = get_local_files_names('D:\OneDrive - ITG Technologies\Desktop\Old Shortcuts')
    
    for file in files:
        print(file)
