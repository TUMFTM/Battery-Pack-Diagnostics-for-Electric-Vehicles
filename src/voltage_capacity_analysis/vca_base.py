# Third Party Imports
from abc import ABC
import scipy as sp
import numpy as np

class VCABase(ABC):
    """
    Voltage Capactiy Analysis base Class
    """
    def __init__(self):
        """
        Init for the Base Class
        """
        # default no filtering input = output
        self.filter_func = lambda x: x
        self.post_filter_func = lambda x: x
        self.mask = None
        self.outlier_detection = lambda x: x

    def differentiate_signal(self,time, signal):
        return np.gradient(signal) / np.gradient(time)

    def calculate_capacity_signal(self,time,current,initial=0):
        # initial in the function is only the first value
        # what I wanted is an offset for the whole signal
        return sp.integrate.cumtrapz(current, time, initial=0) + initial

    def crop_signal_mask(self,signal, limit):
        mask = (signal<limit[0]) | (signal>limit[1])
        return mask

    def apply_mask(self,signal,mask):
        signal = signal[~mask]
        return signal

    def drop_nans_and_infs(self,signal):
        mask_nans = (np.isinf(signal)) | (np.isnan(signal))
        return mask_nans
        #return time[~mask_nans], signal[~mask_nans]

    def normalize_signal(self,signal,factor):
        return signal*factor

    def absolute_signal(self,signal):
        return np.abs(signal)

    def set_filter(self,filter_func):
        # default no filtering input = output
        self.filter_func = filter_func
        return

    def set_post_filter(self,filter_func):
        # default no filtering input = output
        self.post_filter_func = filter_func
        return

    def remove_outlier_IQR(self,signal,percentiles = [5,95]):
        Q1, Q3 = np.percentile(signal, percentiles)
        IQR = Q3 - Q1
        ul = Q3 + 1.5 * IQR
        ll = Q1 - 1.5 * IQR
        outliers = (signal > ul) | (signal < ll)
        return outliers

    def postprocessed_diff_signals(self,time,capacity, voltage):
        dQ = self.differentiate_signal(time,capacity)
        dU = self.differentiate_signal(time,voltage)

        mask_current = self.drop_nans_and_infs(dQ)
        mask_voltage = self.drop_nans_and_infs(dU)

        dQ = self.apply_mask(dQ, mask_current*mask_voltage)
        dU = self.apply_mask(dU, mask_current*mask_voltage)
        time = self.apply_mask(time, mask_current * mask_voltage)
        # mask signal to filter outliers
        outlier_mask_current = self.remove_outlier_IQR(dQ,[25,75])
        outlier_mask_voltage = self.remove_outlier_IQR(dU, [25, 75])

        dQ = self.apply_mask(dQ, outlier_mask_current*outlier_mask_voltage)
        dU = self.apply_mask(dU, outlier_mask_current*outlier_mask_voltage)
        time = self.apply_mask(time, outlier_mask_current*outlier_mask_voltage)
        return time.values, dQ,dU
