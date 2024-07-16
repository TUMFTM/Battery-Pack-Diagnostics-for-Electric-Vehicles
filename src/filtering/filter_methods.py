import numpy as np
import pandas as pd
import scipy.signal as sps
from scipy.signal import butter, lfilter, filtfilt
import scipy.ndimage as spni

from src.filtering.config_filtering import FilteringConfig

class FilterMethods():
    """
    Filter Methods
    """
    def __init__(self):
        pass

    def round_to_next_odd_number(self,window_size):
        return int(np.ceil(window_size) // 2 * 2 + 1)  # round up to next odd number

    def savgol(self,signal,window_size, savgol_dict=FilteringConfig.savgol_dict.value):
        window_size = self.round_to_next_odd_number(window_size)

        return sps.savgol_filter(signal,
                          window_length=window_size,
                          polyorder=savgol_dict["polyorder"],
                          deriv=savgol_dict["deriv"],
                          delta=savgol_dict["delta"],
                          axis=savgol_dict["axis"],
                          mode=savgol_dict["mode"],
                          cval=savgol_dict["cval"])

    def median(self,signal,window_size):
        window_size = self.round_to_next_odd_number(window_size)
        return spni.median_filter(signal,
                          size=window_size)

    def gaussian_filter(self,signal,window_size, std=1, gaussian_dict=FilteringConfig.gaussian_dict.value):
        # for numpy only (e.g. dva, ica)
        window_size = self.round_to_next_odd_number(window_size)
        if type(signal) is not pd.core.frame.DataFrame:
            signal = pd.DataFrame(signal)
        return signal.rolling(window=window_size,
                            win_type="gaussian",
                             **gaussian_dict
                              ).mean(std = std).values.reshape(-1)

    def rolling_mean_df(self,signal,window_size,mean_dict=FilteringConfig.mean_dict.value):
        window_size = self.round_to_next_odd_number(window_size)
        if type(signal) is not pd.core.frame.DataFrame:
            signal = pd.DataFrame(signal)
        return signal.rolling(window=window_size,
                              **mean_dict).mean()

    def rolling_mean_numpy(self, signal, window_size):
        signal = self.rolling_mean_df(signal,window_size)
        return signal.values.reshape(-1)

    def first_order_lowpass(self,signal,cutoff_freq,fs, butter_dict = FilteringConfig.butter_dict.value):
        """
        First Order digital filter
        cutoff_freq = critical frequency in Hz
        fs = sampling frequency in Hz
        """
        b, a = butter(N=1,
                      Wn=cutoff_freq,
                      fs=fs,
                      btype=butter_dict["btype"],
                      analog=butter_dict["analog"])
        return filtfilt(b, a, signal)

    def butter_lowpass(self,signal,cutoff_freq , fs, order, butter_dict = FilteringConfig.butter_dict.value):
        """
        Butterworth digital filter
        N = Order of filter
        cutoff_freq = critical frequency in Hz
        fs = sampling frequency in Hz
        (If fs is specified, Wn is in the same units as fs)
        """
        b, a = butter(N=order,
                      Wn=cutoff_freq,
                      fs=fs,
                      btype=butter_dict["btype"],
                      analog=butter_dict["analog"])
        return filtfilt(b, a, signal) # uses filter forward and backward