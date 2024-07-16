import numpy as np
import pandas as pd
import scipy as sp
from src.filtering.config_filtering import FilteringConfig

class ReadPickle():
    """
    Filter Methods
    """
    def __init__(self):
        # default no filtering input = output
        self.filter_func_I = lambda x: x
        self.filter_func_U = lambda x: x
        self.filter_func_Q = lambda x: x

    def set_filter_I(self, filter_func):
        # default no filtering input = output
        self.filter_func_I = filter_func
        return

    def set_filter_U(self, filter_func):
        # default no filtering input = output
        self.filter_func_U = filter_func
        return

    def set_filter_Q(self, filter_func):
        # default no filtering input = output
        self.filter_func_Q = filter_func
        return

    def calc_Q_from_I(self,df,initial_cap=0):
        df["Q_calc"] = sp.integrate.cumtrapz(df["I"], df["time_h"], initial=0) + initial_cap
        return df

    def filter_cell_voltages(self,df):
        cell_volt_cols =  [col for col in df.columns if "cell_voltage" in col]
        for cell in cell_volt_cols:
            df[cell] = self.filter_func_U(df[cell])
        return df

    def resample_time(self,df,timedelta_s=5):
        df['date'] = pd.to_datetime(df['time_s'], unit='s')
        df.set_index("date",inplace=True)
        timedelta_string = str(timedelta_s)+"s"
        df = df.resample(timedelta_string).first()
        df.reset_index(inplace=True)
        df.drop(columns=["date"], inplace=True)
        return df

    def read(self,path,  initial_cap = 0,resample=False):
        df = pd.read_pickle(path)
        if resample:
            df = self.resample_time(df,resample)
        df["I"] = self.filter_func_I(df["I"])
        df["U"] = self.filter_func_U(df["U"])
        df["Q"] = self.filter_func_Q(df["Q"])
        out = self.filter_cell_voltages(df)
        return out
