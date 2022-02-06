import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import thinkdsp
import fft_eng


def parse_timestamp(ts):
    return np.datetime64(datetime.datetime.strptime(ts, "%m/%d/%Y %H:%M:%S %p"), 'ns')


def parse_file(filename):
    df_data = pd.read_csv(filename)
    df_data['event_id'] = (df_data['Date'] + ' ' + df_data['Time Stamp UTC']).map(parse_timestamp)
    df_data['Relative Time'] = df_data['Relative Time'].map(lambda x: np.timedelta64(round(x * 1000000000), 'ns'))
    df_data['time'] = df_data['event_id'] + df_data['Relative Time']
    df_data['event_id'] = df_data['event_id'].dt.strftime("%Y-%m-%d %H:%M:%S.%f")
    df_data['_ts'] = df_data['time'].dt.strftime("%Y-%m-%d %H:%M:%S.%f")
    df_data = df_data.set_index('time')
    df_data = df_data[['_ts', 'event_id', 'Volt', 'Volt.1', 'Volt.2', 'Volt.3']]
    fs = 1 / (df_data.index[1] - df_data.index[0]).total_seconds()

    return fs, df_data


def get_fft(df_tdw, fs):
    df_fft = df_tdw.loc[:, ['_ts', 'event_id']]

    for meas in ['Volt', 'Volt.1', 'Volt.2', 'Volt.3']:
        tdw = thinkdsp.Wave(ys=df_tdw[meas], ts=df_tdw.index, framerate=fs)
        fft = fft_eng.get_spectrum(wave=tdw, window='kaiser', beta=0, unbias=False, scale_n=True)
        df_fft['FREQ'] = pd.Series(data=fft.fs, index=df_tdw.index[:len(fft.fs)])
        df_fft['_'.join([meas, 'FFT'])] = pd.Series(data=fft.amps, index=df_tdw.index[:len(fft.amps)])

    return df_fft


def main():
    filename = 'C:\\Users\\cmolina\\Downloads\\FAN_CURRENT.csv'
    fs, df_tdw = parse_file(filename)

    df_fft = get_fft(df_tdw, fs)
    df_fft2 = pd.read_csv('C:\\Users\\cmolina\\Downloads\\FAN_FFT.xlsx', skiprows=10)

    # plt.plot(df_fft['FREQ'][df_fft['FREQ']<600], 20*np.log10(df_fft['Volt_FFT'][df_fft['FREQ']<600]), '-')
    plt.plot(df_fft['FREQ'][df_fft['FREQ']<600], df_fft['Volt_FFT'][df_fft['FREQ']<600], '-')
    # plt.plot(df_fft2[df_fft2.columns[0]], df_fft2[df_fft2.columns[1]])  # data from DATAQ (dB)
    plt.plot(df_fft2[df_fft2.columns[0]], df_fft2[df_fft2.columns[2]], '--')  # data from DATAQ (Mag)

    # plt.vlines(x=[x * 60 for x in range(10)], ymin=-200, ymax=100, linestyles='--', colors='grey', alpha=0.5)
    plt.vlines(x=[x * 60 for x in range(10)], ymin=0, ymax=df_fft['Volt_FFT'].max(), linestyles='--', colors='grey', alpha=0.5)

    plt.legend(['my FFT', 'DATAQ FFT', 'Harmonics'])
    plt.show()

    df_fft.to_csv('C:\\Users\\cmolina\\Downloads\\FAN_FFT_ITG.csv')



if __name__ == '__main__':
    main()
