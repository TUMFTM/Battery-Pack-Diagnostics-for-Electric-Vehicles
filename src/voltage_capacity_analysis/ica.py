# Third Party Imports
import numpy as np
import pandas as pd

# First Pary Improts
from src.voltage_capacity_analysis.vca_base import VCABase

class ICA(VCABase):
    """
    Incremental Capacity Analysis Class
    """
    def __init__(self):
        """
        Init for the Base Class
        """
        super(ICA, self).__init__()

    def calc_ica(self, time, capacity, voltage):
        with np.errstate(divide='ignore', invalid='ignore'):
            # it is clear there are dU that are very small and (numerically) lead to a zero division
            # to reduce the error messages this is caught here und the error suppressed (only here)
            # div/0 values are filtered later
            diff_voltage = self.differentiate_signal(time,voltage)
            diff_cap = self.differentiate_signal(time, capacity)
            ica_raw = np.divide(diff_cap, diff_voltage)  # (dQ*dt)/(dU*dt) = dQ/dU
            ica = self.filter_func(ica_raw)
        return ica

    def calc_ica_by_current(self, time, current, voltage):
        diff_voltage = self.differentiate_signal(time,voltage)
        ica_raw = np.divide(current, diff_voltage)  # I*dt/dU = (dQ*dt)/(dU*dt) = dQ/dU
        ica = self.filter_func(ica_raw)
        return ica

    def calc_ica_by_dva(self, time, capacity, voltage):
        diff_voltage = self.differentiate_signal(time, voltage)
        diff_cap = self.differentiate_signal(time, capacity)
        dva = np.divide(diff_voltage,diff_cap)  # (dQ*dt)/(dU*dt) = dQ/dU
        dva_filt = self.filter_func(dva)

        ica = 1/dva_filt
        #ica = self.filter_func(ica)
        return ica

    def get_ica(self, time, capacity, voltage, crop_volt_V=(0,1000), absolute=False, postfilter=False, postfilter_volt_range=(0,5),IQR_filter = True,IQR_percentiles = [5,95]):
        #raw_ica = self.calc_ica(time, capacity, voltage)
        #raw_ica = self.calc_ica_by_current(time, capacity, voltage)
        raw_ica = self.calc_ica_by_dva(time, capacity, voltage)
        ica = self.absolute_signal(raw_ica) if absolute else raw_ica
        # drop nans and filter ica
        mask_nans = self.drop_nans_and_infs(ica)
        ica_no_nan = self.apply_mask(ica, mask_nans)

        if type(voltage) is pd.core.frame.DataFrame:
            # function either takes dataframe or numpy
            # however from here the calculation is based on numpy arrays
            voltage = voltage.values

        voltage_no_nan = self.apply_mask(voltage, mask_nans)

        # mask ica to relevant voltage boundaries
        mask = self.crop_signal_mask(voltage_no_nan, crop_volt_V)
        masked_ica = self.apply_mask(ica_no_nan, mask)
        masked_voltage = self.apply_mask(voltage_no_nan, mask)

        if IQR_filter:
            # mask ica to filter outliers by iqr filter
            outlier_mask = self.remove_outlier_IQR(masked_ica,IQR_percentiles)
            masked_ica = self.apply_mask(masked_ica, outlier_mask)
            masked_voltage = self.apply_mask(masked_voltage, outlier_mask)
        if postfilter:
            mask_post_filt = self.crop_signal_mask(masked_voltage, postfilter_volt_range) # invert mask so inside is filtered
            masked_ica[~mask_post_filt] = self.post_filter_func(masked_ica[~mask_post_filt])
        return np.array(masked_ica), np.array(masked_voltage)

    def get_normalized_ica(self,time, capacity, voltage,crop_volt_V,  scale=1,absolute=False, postfilter=False, postfilter_volt_range=(0,5)):
        ica,voltage = self.get_ica(time, capacity, voltage,crop_volt_V,absolute, postfilter, postfilter_volt_range)
        normalized_ica = self.normalize_signal(ica,scale)
        return normalized_ica, voltage

    def get_cell_ica_from_pack(self,time, capacity, df_cell_voltages, crop_volt_V=(0,1000),
                               absolute=False, postfilter=False, postfilter_volt_range=(0,5)):

        cell_voltages = [col for col in df_cell_voltages.columns if "cell_voltage" in col]

        dict_cell_icas = {}
        for cell in cell_voltages:
            ica_cell, volt_cell = self.get_ica(time=time, capacity = capacity, voltage = df_cell_voltages[cell],
                                               crop_volt_V = crop_volt_V, absolute=absolute,
                                               postfilter=postfilter, postfilter_volt_range=postfilter_volt_range)
            col_name = cell.split("_")[0]+"_ica_"+cell.split("_")[-1]
            dict_cell_icas[col_name] = [volt_cell,ica_cell]

        return dict_cell_icas