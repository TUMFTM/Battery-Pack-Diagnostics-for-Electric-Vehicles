import numpy as np
from src.utils.config_utils import UtilsConfig

class SampleFrequency():
    """
    Calculate the sample frequency of the signal
    """
    def __init__(self):
        pass

    def calc_sample_frequency_estimate(self,time_signal):
        return 1/(np.mean(np.diff(time_signal)))

if __name__ == "__main__":
    time  = np.linspace(0,1,5)
    freq = SampleFrequency().calc_sample_frequency_estimate(time)
    print(f"Sample frequency estimate: {freq} Hz")
