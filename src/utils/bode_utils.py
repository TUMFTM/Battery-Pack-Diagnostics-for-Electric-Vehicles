import numpy as np
from scipy import log10, angle


class Bode():
    """
    Calculate frequencies, fft, angel and amplitude in signal
    inspired by bode_utils library
    """
    def __init__(self):
        pass

    def get_bode_amplitude(self,time, signal, sample_frequency):
        G = self.calc_fft(signal)
        dB_mag, _ = self.calc_dB_mag_and_phase(G)
        freq_array = self.calc_freq_array(time, sample_frequency=sample_frequency)
        return G, dB_mag, freq_array

    def get_bode_phase(self,time, signal, sample_frequency):
        G = self.calc_fft(signal)
        _, phase = self.calc_dB_mag_and_phase(G)
        freq_array = self.calc_freq_array(time, sample_frequency=sample_frequency)
        return G, phase, freq_array

    def calc_dB_mag_and_phase(self,G):
        dB_mag = 20.0 * log10(abs(G))
        phase = angle(G, 1)
        return dB_mag, phase

    def calc_freq_vect_const_ts(self,t):
        dt = t[2] - t[1]
        T = t.max() + dt
        df = 1 / dt
        N = len(t)
        nvect = np.arange(N)
        freq_array = df * nvect
        return freq_array

    def calc_sample_freq_from_t_array(self,time):
        # time in seconds
        norm_time = time-time[0]
        dt = np.mean(np.diff(norm_time))
        #T = norm_time.max() + dt
        freq = 1 / dt
        return freq

    def calc_freq_array(self,time,sample_frequency=None):
        if sample_frequency==None:
            sample_frequency = self.calc_sample_freq_from_t_array(time)
        n_vect = len(time)
        freq_array = np.fft.rfftfreq(n=n_vect, d=1/sample_frequency)
        return freq_array

    def calc_fft(self,signal):
        #Compute the one-dimensional discrete Fourier Transform for real input.
        G = np.fft.rfft(signal)
        return G

    def calc_ifft(self,G):
        return np.fft.irfft(G)