import os.path
import re
# import thinkdsp
import warnings
from datetime import datetime

warnings.simplefilter("ignore", UserWarning)


def isVoltaFile(fileName: str) -> bool:
    return bool(re.search(r"s3://gp-eda-dev-waveform-derivatives/Electrical/Volta", fileName))


def redirectVolta(key: str) -> str:
    bucket = None
    prefixLevel0 = prefixLevel1 = prefixLevel2 = prefixLevel3 = prefixLevel4 = prefixLevel5 = prefixLevel6 = None

    dir, file = os.path.split(key)

    dirMatch = re.search(
        r"s3://(gp-eda-dev-waveform-derivatives)/(Electrical)/(Volta)/(.*)/(MotorReport|MotorStart|MotorStop)", dir)

    if dirMatch:
        bucket = [dirMatch.group(1)]
        prefixLevel0 = [dirMatch.group(2), dirMatch.group(3)]
        prefixLevel2 = [dirMatch.group(5)]

        if dirMatch.group(5) == 'MotorReport':
            fileMatch = re.search(r"Node_\d*_(\d*)_(\d*)_\d*_(tdw-ds|fft-ds|tdw|fft).*", file)

            if fileMatch:
                prefixLevel1 = [fileMatch.group(3)]
                dateMatch = re.search(r"(\d{4})(\d{2})(\d{2})", fileMatch.group(1))

                if dateMatch:
                    prefixLevel3 = [dateMatch.group(1)]
                    prefixLevel4 = [dateMatch.group(2)]
                    prefixLevel5 = [dateMatch.group(3)]

                timeMatch = re.search(r"(\d{2})(\d{2})(\d{2})\d*", fileMatch.group(2))

                if timeMatch:
                    prefixLevel6 = [timeMatch.group(1)]

        elif dirMatch.group(5) == 'MotorStart' or dirMatch.group(5) == 'MotorStop':
            fileMatch = re.search(r"Node_\d*_(\d*)_(\d*)_\d*_.*_(tdw\-ds|fft\-ds|tdw|fft).*", file)

            if fileMatch:
                prefixLevel1 = [fileMatch.group(3)]
                dateMatch = re.search(r"(\d{4})(\d{2})(\d{2})", fileMatch.group(1))

                if dateMatch:
                    prefixLevel3 = [dateMatch.group(1)]
                    prefixLevel4 = [dateMatch.group(2)]
                    prefixLevel5 = [dateMatch.group(3)]

                timeMatch = re.search(r"(\d{2})(\d{2})(\d{2})\d*", fileMatch.group(2))

                if timeMatch:
                    prefixLevel6 = [timeMatch.group(1)]

    return 's3://' + '/'.join(bucket + prefixLevel0 +
                              prefixLevel1 + prefixLevel2 + prefixLevel3 + prefixLevel4 + prefixLevel5 + prefixLevel6 +
                              [file])


def isSELFile(fileName: str) -> bool:
    return bool(re.search(r"s3://gp-eda-dev-waveform-derivatives/Electrical/SEL", fileName))


def redirectSEL(key: str) -> str:
    bucket = None
    prefixLevel0 = prefixLevel1 = prefixLevel2 = prefixLevel3 = prefixLevel4 = prefixLevel5 = prefixLevel6 = None

    dir, file = os.path.split(key)

    dirMatch = re.search(
        r"s3://(gp-eda-dev-waveform-derivatives)/(Electrical)/(SEL)/(.*)/(MotorReport|MotorStart|TransientEvents)", dir)
    if dirMatch:
        bucket = [dirMatch.group(1)]
        prefixLevel0 = [dirMatch.group(2), dirMatch.group(3)]
        prefixLevel2 = [dirMatch.group(5)]

        if dirMatch.group(5) == 'MotorReport' or dirMatch.group(5) == 'MotorStart':
            # 210208,063148848702,0,Brewton,710_5_C1_0_068M,GP,CMET_S_R_tdw.csv
            fileMatch = re.search(r"(\d*),(\d*),0,(\w*),(.*),(GP),(CMET_S_R|MSR)_(tdw\-ds|fft\-ds|tdw|fft).*", file)

            if fileMatch:
                prefixLevel1 = [fileMatch.group(7)]

                dateStr = datetime.strptime(fileMatch.group(1), "%y%m%d").strftime("%Y%m%d")
                dateMatch = re.search(r"(\d{4})(\d{2})(\d{2})", dateStr)

                if dateMatch:
                    prefixLevel3 = [dateMatch.group(1)]
                    prefixLevel4 = [dateMatch.group(2)]
                    prefixLevel5 = [dateMatch.group(3)]

                timeMatch = re.search(r"(\d{2})(\d{2})(\d{2})\d*", fileMatch.group(2))

                if timeMatch:
                    prefixLevel6 = [timeMatch.group(1)]

        elif dirMatch.group(5) == 'TransientEvents':
            # SEL_event_10000_20210829223709659548_SEL710-C1-1-179M_fft.csv
            fileMatch = re.search(r"SEL_event_\d*_(\d*)_(.*)_(tdw\-ds|fft\-ds|tdw|fft).*", file)

            if fileMatch:
                prefixLevel1 = [fileMatch.group(3)]

                dateMatch = re.search(r"(\d{4})(\d{2})(\d{2})\d*", fileMatch.group(1))

                if dateMatch:
                    prefixLevel3 = [dateMatch.group(1)]
                    prefixLevel4 = [dateMatch.group(2)]
                    prefixLevel5 = [dateMatch.group(3)]

                timeMatch = re.search(r"\d{4}\d{2}\d{2}(\d{2})(\d{2})(\d{2})\d*", fileMatch.group(1))

                if timeMatch:
                    prefixLevel6 = [timeMatch.group(1)]

    return 's3://' + '/'.join(bucket + prefixLevel0 +
                              prefixLevel1 + prefixLevel2 + prefixLevel3 + prefixLevel4 + prefixLevel5 + prefixLevel6 +
                              [file])


def isKCFFile(fileName: str) -> bool:
    return bool(re.search(r"s3://gp-eda-dev-waveform-derivatives/Vib/KCF", fileName))


def redirectKCF(key: str) -> str:
    bucket = prefix = None
    fileMatch = None

    dir, file = os.path.split(key)

    dirMatch = re.search(r"s3://(gp-eda-dev-waveform-derivatives)/(Electrical)/(Volta)/"
                         r"(.*)/(MotorReport|MotorStart|MotorStop)", dir)

    if dirMatch.group(5) == 'MotorReport':
        fileMatch = re.search(r"Node_\d*_(\d*)_(\d*)_\d*_(tdw\-ds|fft\-ds|tdw|fft).*", file)
    elif dirMatch.group(5) == 'MotorStart' or dirMatch.group(5) == 'MotorStop':
        fileMatch = re.search(r"Node_\d*_(\d*)_(\d*)_\d*_.*_(tdw\-ds|fft\-ds|tdw|fft).*", file)

    dateMatch = re.search(r"(\d{4})(\d{2})(\d{2})", fileMatch.group(1))
    timeMatch = re.search(r"(\d{2})(\d{2})(\d{2})", fileMatch.group(2))

    if dirMatch and fileMatch and dateMatch and timeMatch:
        bucket = [dirMatch.group(1)]
        prefix = [dirMatch.group(2), dirMatch.group(3), fileMatch.group(3), dirMatch.group(5), dateMatch.group(1),
                  dateMatch.group(2), dateMatch.group(3), timeMatch.group(1), file]

    return 's3://' + '/'.join(bucket + prefix)


def isBannerFile(fileName: str) -> bool:
    return bool(re.search(r"s3://gp-eda-dev-waveform-derivatives/Vib/Banner", fileName))


def redirectBanner(key: str) -> str:
    bucket = prefix = None
    fileMatch = None

    dir, file = os.path.split(key)

    dirMatch = re.search(r"s3://(gp-eda-dev-waveform-derivatives)/(Electrical)/(Volta)/"
                         r"(.*)/(MotorReport|MotorStart|MotorStop)", dir)

    if dirMatch.group(5) == 'MotorReport':
        fileMatch = re.search(r"Node_\d*_(\d*)_(\d*)_\d*_(tdw\-ds|fft\-ds|tdw|fft).*", file)
    elif dirMatch.group(5) == 'MotorStart' or dirMatch.group(5) == 'MotorStop':
        fileMatch = re.search(r"Node_\d*_(\d*)_(\d*)_\d*_.*_(tdw\-ds|fft\-ds|tdw|fft).*", file)

    dateMatch = re.search(r"(\d{4})(\d{2})(\d{2})", fileMatch.group(1))
    timeMatch = re.search(r"(\d{2})(\d{2})(\d{2})", fileMatch.group(2))

    if dirMatch and fileMatch and dateMatch and timeMatch:
        bucket = [dirMatch.group(1)]
        prefix = [dirMatch.group(2), dirMatch.group(3), fileMatch.group(3), dirMatch.group(5), dateMatch.group(1),
                  dateMatch.group(2), dateMatch.group(3), timeMatch.group(1), file]

    return 's3://' + '/'.join(bucket + prefix)


def main():
    '''  keys  '''
    volta_key = ''
    volta_key = 's3://gp-eda-dev-waveform-derivatives/Electrical/Volta/FFT/MotorReport/Node_21000_20200819_060000_1597816800_fft.csv'
    volta_key = 's3://gp-eda-dev-waveform-derivatives/Electrical/Volta/FFT/MotorStart/Node_21000_20200819_060000_1597816800_start_fft.csv'
    volta_key = 's3://gp-eda-dev-waveform-derivatives/Electrical/Volta/FFT/MotorStop/Node_21000_20200819_060000_1597816800_stop-u_fft-ds_red-rate=01.csv'

    sel_key = ''
    # sel_key = 's3://gp-eda-dev-waveform-derivatives/Electrical/SEL/FFT/TransientEvents/SEL_event_10000_20210829223709659548_SEL710-C1-1-179M_tdw-ds_red-rate=09.csv'
    # sel_key = 's3://gp-eda-dev-waveform-derivatives/Electrical/SEL/FFT/MotorReport/210208,063148848702,0,Brewton,710_5_C1_0_068M,GP,CMET_S_R_fft.csv'
    # sel_key = 's3://gp-eda-dev-waveform-derivatives/Electrical/SEL/FFT/MotorStart/210107,152351795602,0,Brewton,710_5_C1_0_067M,GP,MSR_tdw.csv'

    kcf_key = ''
    # kcf_key = 's3://gp-eda-dev-waveform-derivatives/Vibe/KCF/FFT/facility_name=BRUNSWICK CELLULOSE/dim_date_key=20220207/part-00032-2771e224-d68f-4540-9666-f473f6a7ce87.c000.snappy_node-id=00002D92_fft.csv'

    if isVoltaFile(volta_key):
        print('key: \t\t', volta_key)
        volta_key = redirectVolta(volta_key)
        print('new key: \t', volta_key)

    if isSELFile(sel_key):
        print('key: \t\t', sel_key)
        sel_key = redirectSEL(sel_key)
        print('new key: \t', sel_key)

    if isKCFFile(kcf_key):
        print('key: \t\t', kcf_key)
        kcf_key = redirectKCF(kcf_key)
        print('new key: \t', kcf_key)


if __name__ == '__main__':
    main()
