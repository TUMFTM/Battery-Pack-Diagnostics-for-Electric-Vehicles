from src.data.read_pickle import ReadPickle
import pandas as pd
import scipy as sp

class ReadFeather(ReadPickle):
    """
    Filter Methods
    """
    def __init__(self):
        super(ReadFeather, self).__init__()

    def read(self,path,  initial_cap = 0,resample=False):
        df = pd.read_feather(path)
        if resample:
            df = self.resample_time(df,resample)
        df["I"] = self.filter_func_I(df["I"])
        df["U"] = self.filter_func_U(df["U"])
        df["Q"] = self.filter_func_Q(df["Q"])
        out = self.filter_cell_voltages(df)
        return out