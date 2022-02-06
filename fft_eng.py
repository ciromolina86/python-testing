import thinkdsp
import numpy as np
from scipy.signal import hilbert
from typing import Union
import lttb


def get_wave(spectrum: thinkdsp.Spectrum, scale_n: bool = False, scale_rms: bool = False,
             scale_ortho: bool = False) -> thinkdsp.Wave:
    """
    Reconstructing wave back from spectrum object

    :param scale_n: scaling to be applied to spectrum magnitude
    :param scale_rms: scaling to be applied to spectrum magnitude
    :param scale_ortho: scaling to be applied to spectrum magnitude
    :param spectrum: Spectrum object

    :return: Wave object
    """

    # create a copy of the original spectrum
    s = spectrum.copy()

    # removing the attenuation due to the FFT algorithm
    n = len(s)

    # apply scaling to spectrum
    if scale_ortho:
        s.scale(np.sqrt(n))
    if scale_rms:
        s.scale(np.sqrt(2))
    if scale_n:
        s.scale(n)

    # returns the reconstructed wave
    return s.make_wave()


def get_spectrum(wave: thinkdsp.Wave, window: str = '', beta: Union[int, float] = 6, normalize: bool = False,
                 amp: float = 1.0, unbias: bool = False, scale_n: bool = False, scale_rms: bool = False,
                 scale_ortho: bool = False) -> thinkdsp.Spectrum:
    """
    Get a spectrum from an given wave

    :param unbias: unbias wave (remove DC level)
    :param amp: amplitude to normalize wave to
    :param normalize: normalize wave to amp amplitude
    :param wave: Wave object
    :param window: windowing string, default is 'hanning'. e.g. 'hanning', 'blackman', 'bartlett', 'kaiser'
    :param beta: beta parameter for kaiser windowing
    :param scale_n: scaling to be applied to spectrum magnitude
    :param scale_rms: scaling to be applied to spectrum magnitude
    :param scale_ortho: scaling to be applied to spectrum magnitude

    :return: Spectrum object
    """

    # create a copy of the original wave
    tdw = wave.copy()

    # unbiases the signal
    if unbias:
        tdw.unbias()

    # normalizes the signal
    if normalize:
        tdw.normalize(amp=amp)

    # apply user defined window to the time domain waveform
    if window == 'hanning':
        '''The Hanning window is a taper formed by using a weighted cosine'''

        tdw.window(np.hanning(len(tdw.ys)))

    if window == 'blackman':
        '''The Blackman window is a taper formed by using the first three terms of a summation of cosines. 
        It was designed to have close to the minimal leakage possible. 
        It is close to optimal, only slightly worse than a Kaiser window'''

        tdw.window(np.blackman(len(tdw.ys)))

    if window == 'bartlett':
        '''The Bartlett window is very similar to a triangular window, 
        except that the end points are at zero. It is often used in signal processing for tapering a signal, 
        without generating too much ripple in the frequency domain.'''

        tdw.window(np.bartlett(len(tdw.ys)))

    if window == 'kaiser':
        '''The Kaiser window is a taper formed by using a Bessel function.
        beta    Window shape
        0	    Rectangular
        5	    Similar to a Hamming
        6	    Similar to a Hanning
        8.6	    Similar to a Blackman '''

        tdw.window(np.kaiser(len(tdw.ys), beta=beta))

    # obtain the spectrum from a wave
    result = tdw.make_spectrum(full=False)

    n = len(result)

    # apply scaling to spectrum
    if scale_ortho:
        result.scale(1 / np.sqrt(n))
    if scale_rms:
        result.scale(1 / np.sqrt(2))
    if scale_n:
        result.scale(1 / n)

    # returns a Spectrum object
    return result


def demodulation_wave(wave, fc1=400, fc2=800):
    """
    Computes the envelope of a wave (fc1<freq<fc2)

    :param wave: thinkdsp.Wave object
    :param fc1: first cutoff frequency
    :param fc2: second cutoff frequency
    :return: thinkdsp.Spectrum object
    """

    # create a copy of the original wave
    raw_wave = wave.copy()

    # make a spectrum from  wave
    raw_spectrum = raw_wave.make_spectrum(full=False)

    # apply a high pass filter at fc1 to the raw spectrum
    raw_spectrum.high_pass(fc1)
    raw_spectrum.low_pass(fc2)

    # make a time waveform from the filtered spectrum
    raw_wave_filtered = raw_spectrum.make_wave()
    # apply hanning windowing to the result waveform
    raw_wave_filtered.window(np.hanning(len(raw_wave_filtered)))

    # obtain the envelop of the result waveform
    raw_wave_filtered_envelop = thinkdsp.Wave(ys=np.abs(hilbert(raw_wave_filtered.ys)),
                                              ts=raw_wave_filtered.ts,
                                              framerate=raw_wave_filtered.framerate)

    # obtain the spectrum from the envelop
    result = raw_wave_filtered_envelop.make_spectrum(full=False)

    # returns the result
    return result


def demodulation_spectrum(spectrum, fc1=400, fc2=800):
    """
    Computes the envelope of a spectrum (fc1<freq<fc2)

    :param spectrum: thinkdsp.Spectrum object
    :param fc1: first cutoff frequency
    :param fc2: second cutoff frequency
    :return: tinkdsp.Spectrum object
    """

    # make a spectrum copy of the original spectrum
    raw_spectrum = spectrum.copy()

    # apply a high pass filter at fc1 to the raw spectrum
    raw_spectrum.high_pass(fc1)
    raw_spectrum.low_pass(fc2)

    # make a time waveform from the filtered spectrum
    raw_wave_filtered = raw_spectrum.make_wave()
    # apply hanning windowing to the result waveform
    raw_wave_filtered.window(np.hanning(len(raw_wave_filtered)))

    # obtain the envelop of the result waveform
    raw_wave_filtered_envelop = thinkdsp.Wave(ys=np.abs(hilbert(raw_wave_filtered.ys)), ts=raw_wave_filtered.ts,
                                              framerate=raw_wave_filtered.framerate)

    # obtain the spectrum from the envelop
    result = raw_wave_filtered_envelop.make_spectrum(full=False)

    # returns the result
    return result


def spectrum_to_dict(s):
    """
    Returns a given dictionary of a spectrum object

    :param s: thinkdsp.Spectrum object
    :return: result dictionary
    """

    # create a result dictionary
    result = {}
    result.update({'real': s.real})
    result.update({'imag': s.imag})
    result.update({'angles': s.angles})
    result.update({'amps': s.amps})
    result.update({'power': s.power})
    result.update({'freqs': s.fs})

    return result


def wave_to_dict(w):
    """
    Returns a given dictionary of a wave object

    :param w: thinkdsp.Wave object
    :return: result dictionary
    """

    # create a result dictionary
    result = {}
    result.update({'samples': w.ys})
    result.update({'sample_time': w.ts})
    result.update({'fs': w.framerate})

    return result


def diff_wave(w0, w1):
    """
    Computes and returns the  difference between waves w1-w0.

    :param w0: wave 0
    :param w1: wave 1
    :return: wave difference
    """

    # returns result wave
    return thinkdsp.Wave(ys=np.abs(w1.ys - w0.ys), ts=w0.ts, framerate=w0.framerate)


def diff_spectrum(s0, s1):
    """
    Computes and returns the  difference between spectra s1-s0.

    :param s0: spectrum 0
    :param s1: spectrum 1
    :return: wave difference
    """

    # returns result spectrum
    return thinkdsp.Spectrum(hs=np.abs(s1.amps - s0.amps), fs=s0.fs, framerate=s0.framerate)


def integrate(w: thinkdsp.Wave) -> thinkdsp.Wave:
    """
    Integrate time domain wave

    :param w: Wave object
    :return: Wave object
    """

    # creates a copy of the original wave
    xt = w.copy()

    # gets its spectrum
    xf = xt.make_spectrum(full=False)

    # applies an integration filter
    yf = xf.integrate()

    # replaces the NaN value (due to division by zero) with zero
    yf.hs[0] = 0

    # reconstructs its wave after being integrated
    yt = yf.make_wave()

    # returns the new integrated wave
    return yt


def derivate(w: thinkdsp.Wave) -> thinkdsp.Wave:
    """
    Derivate time domain wave

    :param w: Wave object
    :return: Wave object
    """

    # creates a copy of the original wave
    xt = w.copy()

    # gets its spectrum
    xf = xt.make_spectrum(full=False)

    # applies an differentiation filter
    yf = xf.differentiate()

    # reconstructs its wave after being derivated
    yt = yf.make_wave()

    # returns the new integrated wave
    return yt


def get_col_and_rows_numpy_array(numpy_array):
    """

    :param numpy_array:
    :return:
    """
    # Check Array Dimension
    numpy_array_dim = numpy_array.ndim

    if numpy_array_dim == 2:
        # Get number of columns of the numpy array
        numpy_array_row, numpy_array_col = numpy_array.shape
    elif numpy_array_dim == 1:
        numpy_array_row = numpy_array.size
        numpy_array_col = 1
    else:
        numpy_array_row = 0
        numpy_array_col = 0
        print("Error: Wrong Input Matrix Dimension")

    return numpy_array_row, numpy_array_col


def dataset_downsampling_lttb_ts(np, data_v_in, data_ts_in, overview_max_datapoints, row_count_in, column_count_in):
    """

    :param np:
    :param data_v_in:
    :param data_ts_in:
    :param overview_max_datapoints:
    :param row_count_in:
    :param column_count_in:
    :return:
    """

    #############################################################################
    # Down-sampling Data Set if it is needed
    #############################################################################
    # Get number of  data points
    datapoints_count = int(column_count_in) * int(row_count_in)
    overview_max_row = int(int(overview_max_datapoints) / int(column_count_in))

    if datapoints_count > overview_max_datapoints:
        # Create Index Array
        data_v = data_v_in.copy()
        data_ts = data_ts_in.copy()
        ind = np.linspace(1, len(data_v[:, 0]), len(data_v[:, 0]))
        ind = np.asmatrix(ind)
        ind = ind.T

        # Concatenate Index and Data Value array
        data_v = np.concatenate((ind, data_v), axis=1)

        # Convert to array
        data_v = np.asarray(data_v)
        data_ts = np.asarray(data_ts)

        # Downsample using LTTB
        data_v_out_tmp, data_ts_out = lttb.lttb_downsample_ts(np, data_v, data_ts, overview_max_row)

        # Check Array Dimension for Array with real values
        data_v_out_dim = data_v_out_tmp.ndim

        if data_v_out_dim == 2:
            # Get number of columns of the numpy array
            data_v_out_row, data_v_out_col = data_v_out_tmp.shape
        elif data_v_out_dim == 1:
            data_v_out_col = 1
        else:
            data_v_out_col = 0
            print("Error: Wrong Input Matrix Dimension")

        # Remove Index Column
        data_v_out = data_v_out_tmp[:, 1:data_v_out_col]

    else:
        data_v_out = data_v_in.copy()
        data_ts_out = data_ts_in.copy()

    # Transform to numpy matrix
    data_v_out = np.asmatrix(data_v_out)
    data_ts_out = np.asmatrix(data_ts_out)

    return data_v_out, data_ts_out


def dataset_downsampling_lttb(np, data_v_in, overview_max_datapoints, row_count_in, column_count_in):
    """

    :param np:
    :param data_v_in:
    :param overview_max_datapoints:
    :param row_count_in:
    :param column_count_in:
    :return:
    """

    #############################################################################
    # Down-sampling Data Set if it is needed
    #############################################################################
    # Get number of  data points
    datapoints_count = int(column_count_in) * int(row_count_in)
    overview_max_row = int(int(overview_max_datapoints) / int(column_count_in))

    if datapoints_count > overview_max_datapoints:
        # Create Index Array
        data_v = data_v_in.copy()
        ind = np.linspace(1, len(data_v[:, 0]), len(data_v[:, 0]))
        ind = np.asmatrix(ind)
        ind = ind.T

        # Concatenate Index and Data Value array
        data_v = np.concatenate((ind, data_v), axis=1)

        # Convert to array
        data_v = np.asarray(data_v)

        # Downsample using LTTB
        data_v_out_tmp = lttb.lttb_downsample(np, data_v, overview_max_row)

        # Check Array Dimension for Array with real values
        data_v_out_dim = data_v_out_tmp.ndim

        if data_v_out_dim == 2:
            # Get number of columns of the numpy array
            data_v_out_row, data_v_out_col = data_v_out_tmp.shape
        elif data_v_out_dim == 1:
            data_v_out_col = 1
        else:
            data_v_out_col = 0
            print("Error: Wrong Input Matrix Dimension")

        # Remove Index Column
        data_v_out = data_v_out_tmp[:, 1:data_v_out_col]

    else:
        data_v_out = data_v_in.copy()

    return data_v_out


def split_fft_based_on_bin(pd, config_param, fft_pdf_list, fft_names_list):
    """

    :param pd:
    :param config_param:
    :param fft_pdf_list:
    :param fft_names_list:
    :return:
    """

    # Initialization
    num_bins = config_param.get('num_bins')
    acc_bins_col_names_list = []
    vel_bins_col_names_list = []

    # Get numpy matrix from pdf list
    acc_fft_mtx_pdf = fft_pdf_list[0]
    acc_fft_mtx = acc_fft_mtx_pdf[fft_names_list[0]].values
    vel_fft_mtx_pdf = fft_pdf_list[1]
    vel_fft_mtx = vel_fft_mtx_pdf[fft_names_list[1]].values

    # Get matrix shape
    acc_fft_mtx_rows, acc_fft_mtx_col = get_col_and_rows_numpy_array(acc_fft_mtx)
    vel_fft_mtx_rows, vel_fft_mtx_col = get_col_and_rows_numpy_array(vel_fft_mtx)

    # Reshape to 1 column
    acc_fft_mtx = np.reshape(acc_fft_mtx, (acc_fft_mtx_rows, 1))
    vel_fft_mtx = np.reshape(vel_fft_mtx, (vel_fft_mtx_rows, 1))
    acc_fft_mtx = np.asmatrix(acc_fft_mtx)
    vel_fft_mtx = np.asmatrix(vel_fft_mtx)

    # Calculate bin size
    acc_bins_size = int(acc_fft_mtx_rows / num_bins)
    vel_bins_size = int(vel_fft_mtx_rows / num_bins)

    # Reduce matrix
    acc_fft_mtx_reduced = acc_fft_mtx[0:num_bins * acc_bins_size]
    vel_fft_mtx_reduced = vel_fft_mtx[0:num_bins * vel_bins_size]

    # Split fft reduced (fft only get reduced if the number of rows is not a multiple of the number of bins)
    acc_new_fft_mtx_list = np.array_split(acc_fft_mtx_reduced, num_bins)
    vel_new_fft_mtx_list = np.array_split(vel_fft_mtx_reduced, num_bins)

    # Convert list to matrix
    acc_fft_mtx_bins = None
    vel_fft_mtx_bins = None
    for acc_mtx_index, vel_mtx_index in zip(range(len(acc_new_fft_mtx_list)), range(len(vel_new_fft_mtx_list))):
        if acc_mtx_index == 0 and vel_mtx_index == 0:
            acc_fft_mtx_bins = acc_new_fft_mtx_list[acc_mtx_index]
            vel_fft_mtx_bins = vel_new_fft_mtx_list[vel_mtx_index]
        else:
            acc_fft_mtx_bins = np.concatenate((acc_fft_mtx_bins, acc_new_fft_mtx_list[acc_mtx_index]), axis=1)
            vel_fft_mtx_bins = np.concatenate((vel_fft_mtx_bins, vel_new_fft_mtx_list[vel_mtx_index]), axis=1)

    # Get bins matrix shape
    acc_fft_mtx_bins_rows, acc_fft_mtx_bins_col = get_col_and_rows_numpy_array(acc_fft_mtx_bins)
    vel_fft_mtx_bins_rows, vel_fft_mtx_bins_col = get_col_and_rows_numpy_array(vel_fft_mtx_bins)

    # Create column names for the bins matrix
    for acc_bin_num_index, vel_bin_num_index in zip(range(len(acc_new_fft_mtx_list)), range(len(vel_new_fft_mtx_list))):
        # Create column names for bins
        acc_bins_col_names_list.append(fft_names_list[0] + "_BIN" + str(acc_bin_num_index))
        vel_bins_col_names_list.append(fft_names_list[1] + "_BIN" + str(vel_bin_num_index))

    # Cast always to float
    acc_fft_mtx_bins = acc_fft_mtx_bins.astype(float)
    vel_fft_mtx_bins = vel_fft_mtx_bins.astype(float)

    # Create dataframe for the fft split bins (acc and vel)
    acc_fft_pdf_bins = pd.DataFrame(data=acc_fft_mtx_bins, columns=acc_bins_col_names_list,
                                    index=acc_fft_mtx_pdf.index[:acc_fft_mtx_bins_rows])
    vel_fft_pdf_bins = pd.DataFrame(data=vel_fft_mtx_bins, columns=vel_bins_col_names_list,
                                    index=vel_fft_mtx_pdf.index[:vel_fft_mtx_bins_rows])

    return acc_fft_pdf_bins, vel_fft_pdf_bins


def required_config_info_status(config_model, asset):
    """

    :param config_model:
    :param asset:
    :return:
    """
    # Check if required configuration is sde tag configuration
    if 'CFG' not in config_model[asset]:
        required_config = False
    else:
        if 'FS' not in config_model[asset]['CFG'] or 'N_TDW' not in config_model[asset]['CFG']:
            required_config = False
        else:
            required_config = True

    return required_config
