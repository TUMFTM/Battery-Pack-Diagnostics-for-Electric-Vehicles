# Third Party Imports
import scipy as sp
from scipy.interpolate import interp1d
import numpy as np
import pandas as pd

# First Pary Improts
from src.voltage_capacity_analysis.vca_base import VCABase
from src.filtering.filter_methods import FilterMethods

class DVA(VCABase,FilterMethods):
    """
    Differential Voltage Analysis Class
    """
    def __init__(self):
        """
        Init for the Base Class
        """
        super(DVA, self).__init__()
        self.Q_max = 1

    def calc_dva(self,time, capacity, voltage):
        diff_voltage = self.differentiate_signal(time, voltage)
        diff_cap = self.differentiate_signal(time, capacity)
        dva = np.divide(diff_voltage, diff_cap)  # (dU*dt)/(dQ*dt) = dU/dQ
        return dva

    def calc_dva_by_current(self,time, current, voltage):
        diff_voltage = self.differentiate_signal(time, voltage)
        dva = np.divide(diff_voltage, current)  # dU/(dt*I) = (dU*dt)/(dQ*dt) = dU/dQ
        return dva

    def calc_dva_by_interpolation(self,capacity,voltage):
        # DVA-Calculation using difference quotient
        # Length of Ah-step for computation of differences quotient (standard value - literature: 0.1-0.2% of total capacity)
        Ah_step_length = 0.002  # Length of Ah-step
        delta_Ah = abs(max(capacity) * Ah_step_length)  # delta_Ah for calculation of difference quotient
        # Calculation of difference quotient of filtered OCV
        int_funct_DVA = interp1d(capacity, voltage, fill_value="extrapolate")
        dva = (int_funct_DVA(capacity + delta_Ah) - int_funct_DVA(capacity - delta_Ah)) / (2*delta_Ah)
        return dva

    def get_dva(self, time, capacity, voltage, crop_cap_Ah=(0,165), absolute=False,
                return_soc = False, soc_signal=None, soc_offset=0,
                postfilter=False, postfilter_cap_range=(10,100)):

        self.Q_max = capacity.values[-1]
        raw_dva = self.calc_dva(time, capacity, voltage)
        dva = self.absolute_signal(raw_dva) if absolute else raw_dva

        filtered_dva = self.filter_func(dva)
        # crop Ah
        mask = self.crop_signal_mask(capacity, crop_cap_Ah)
        masked_dva = self.apply_mask(filtered_dva, mask)
        masked_capacity = self.apply_mask(capacity, mask)

        if postfilter:
            # invert mask so inside is filtered
            mask_post_filt = self.crop_signal_mask(masked_capacity, postfilter_cap_range)
            masked_dva[~mask_post_filt] = self.post_filter_func(masked_dva[~mask_post_filt])

        if return_soc:
            masked_capacity = self.apply_mask(soc_signal, mask)+soc_offset

        return masked_dva, masked_capacity

    def get_normalized_dva(self,time, capacity, voltage,
                           crop_cap_Ah=(0,165), absolute=False,
                           return_soc = False,soc_offset=0,
                           postfilter=False, postfilter_cap_range=(10,100)):
        dva, capacity_signal = self.get_dva(time, capacity, voltage,crop_cap_Ah, absolute,return_soc,soc_offset, postfilter, postfilter_cap_range)
        normalized_dva = self.normalize_signal(dva,self.Q_max)
        return normalized_dva, capacity_signal

    def get_cell_dva_from_pack(self,time, capacity, df_cell_voltages, crop_cap_Ah=(0,165), absolute=False,
                               return_soc = False, soc_signal=None, soc_offset=0,
                               postfilter=False, postfilter_cap_range=(10,100)):

        cell_voltages = [col for col in df_cell_voltages.columns if "cell_voltage" in col]
        # get the capacity signal of one cell, as this will be the same for all cells, due to one current sensor per pack
        _,cap = self.get_dva(time=time, capacity=capacity, voltage=df_cell_voltages[cell_voltages[0]],
                     crop_cap_Ah=crop_cap_Ah, absolute=absolute,
                     return_soc=return_soc, soc_signal=soc_signal, soc_offset=soc_offset,
                     postfilter=postfilter, postfilter_cap_range=postfilter_cap_range)

        dfs_cell_dvas = [pd.DataFrame(cap.to_numpy(), columns=["Q"])]
        for cell in cell_voltages:
            dva_cell, _ = self.get_dva(time=time, capacity = capacity, voltage = df_cell_voltages[cell],
                                              crop_cap_Ah=crop_cap_Ah, absolute=absolute,
                                                return_soc=return_soc, soc_signal=soc_signal, soc_offset=soc_offset,
                                                postfilter=postfilter, postfilter_cap_range=postfilter_cap_range)
            col_name = cell.split("_")[0]+"_dva_"+cell.split("_")[-1]
            dfs_cell_dvas.append(pd.DataFrame(dva_cell,columns=[col_name]))

        df_cell_dvas = pd.concat(dfs_cell_dvas,axis=1)
        return df_cell_dvas

    def get_soc_vector(self, capacity,soc_offset):
        Q_x = [capacity[0],capacity[-1]]
        SOC_y = [soc_offset,100]

        soc = np.interp(capacity, Q_x, SOC_y)
        return soc

    def get_graphite_peak_location(self,capa,dva,thres1,thres2,n_parallel=1):
        max_dva = np.max(dva[(capa > thres1) & (capa < thres2)])  # depends on cell or vehicle
        return capa[(capa > thres1) & (dva == max_dva)].iloc[0] / n_parallel

    def get_Q_shift_for_lower_cut_off_voltage(self,df_vehicle,df_cell,n_seriell=1,n_parallel=1):
        return (n_parallel*df_cell["Q"][df_cell['U'].sub(np.min(df_vehicle["U"]/n_seriell)).abs().idxmin()]) - np.min(df_vehicle["Q"])

    def strech_capa_signal(self,capa,strech_factor,abs_pos_grafit_peak):
        mask_below_grafit_peak = capa<abs_pos_grafit_peak
        section_left_of_grafit_peak = capa[mask_below_grafit_peak]-abs_pos_grafit_peak # zero base signal
        section_left_of_grafit_peak = section_left_of_grafit_peak*strech_factor
        capa[mask_below_grafit_peak] = section_left_of_grafit_peak+abs_pos_grafit_peak #shift back
        return capa
