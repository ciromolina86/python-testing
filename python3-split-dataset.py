import os.path
import pandas as pd


def splitDataset(fileName: str, noOfRecords: int) -> None:
    """
    Split a big dataset file into multiple smaller dataset files

    :param fileName: source file name
    :param noOfRecords: maximum number of records of the destination files
    :return: None
    """
    _fileName, _ext = os.path.splitext(fileName)

    for i, chunk in enumerate(pd.read_csv(fileName, chunksize=noOfRecords)):
        chunk.to_csv(f'{_fileName}.{i+1:03}.csv', index=False)


if __name__ == '__main__':
    fileName = input('Enter full file path: ')
    noOfRecords = int(input('Enter number of records: '))

    splitDataset(fileName=fileName, noOfRecords=1_000_000)
