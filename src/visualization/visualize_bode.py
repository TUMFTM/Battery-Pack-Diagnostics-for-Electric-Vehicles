from src.visualization.config_visualization import VisualizationConfig
from src.utils.bode_utils import Bode
from bode_utils import bode_plot2, set_db_ticks, set_log_ticks, set_phase_ticks
import matplotlib.pyplot as plt

class VisualizeBode(Bode):
    """
    create the bode plot
    inspired by bode_utils library
    """
    def __init__(self):
        super(VisualizeBode, self).__init__()

    def get_bode_plot(self,time, signal,len_freq=None):
        G = self.calc_fft(signal)
        freq_array = self.calc_freq_array(time,len_freq)
        db1, phase1 = bode_plot2(freq_array, G)
        return db1, phase1

    def get_bode_phase_plot(self, time, signal,sample_frequency=None,axes=None, label=None, linestyle="-", xlim=None,ylim=None, **kwargs):
        G, phase, freq_array = self.get_bode_phase(time, signal, sample_frequency)
        return self.bode_plot(freq_array, phase, "phase", axes, label, linestyle, xlim,ylim, **kwargs)

    def get_bode_amplitude_plot(self, time, signal,sample_frequency=None, axes=None, label=None, linestyle="-", xlim=None,ylim=None, **kwargs):
        G, dB_mag, freq_array = self.get_bode_amplitude(time, signal, sample_frequency)
        return self.bode_plot(freq_array, dB_mag, "mag", axes, label, linestyle, xlim,ylim, **kwargs)

    def get_bode_amplitude_2col(self, time, signal1, signal2,sample_frequency1=None, sample_frequency2=None, axes=None, label=None, linestyle="-", xlim=None,ylim=None, **kwargs):
        try:
            if not axes:
                _, axes = plt.subplots(1, 2,
                                     figsize=(VisualizationConfig.col_width_two_col_doc_in_cm.value,  # width
                                              VisualizationConfig.height.value))  # heigth
        except:
            pass

        G1 = self.calc_fft(signal1)
        dB_mag1, _ = self.calc_dB_mag_and_phase(G1)
        freq_array1 = self.calc_freq_array(time,sample_frequency=sample_frequency1)
        self.bode_plot(freq_array1, dB_mag1, "mag",axes[0], label, linestyle, xlim,ylim,title="Current", **kwargs)

        G2 = self.calc_fft(signal2)
        dB_mag2, _ = self.calc_dB_mag_and_phase(G2)
        freq_array2 = self.calc_freq_array(time,sample_frequency=sample_frequency2)
        self.bode_plot(freq_array2, dB_mag2, "mag", axes[1],None, linestyle, xlim, ylim,title="Voltage", **kwargs)
        return axes

    def bode_plot(self, freq_array, signal, type, axes=None, label=None, linestyle="-", xlim=None, ylim=None,title=None, **kwargs):
        if not axes:
            _, axes = plt.subplots(1, 1,
                                 figsize=(VisualizationConfig.col_width_one_col_doc_in_inch.value,  # width
                                          VisualizationConfig.height.value))  # heigth

        axes.semilogx(freq_array, signal, linestyle, label=label, **kwargs)
        axes.grid(color="gainsboro",which="both")
        axes.set_axisbelow(True)
        axes.set_xlabel('Freq. (Hz)')

        set_log_ticks(axes, nullx=False)

        if type == "mag":
            axes.set_ylabel("dB Mag.")
            #set_db_ticks(axes, signal)
        elif type == "phase":
            axes.set_ylabel('Phase (deg.)')
            set_phase_ticks(axes, signal)
        else:
            print("Plot type not supported")

        if xlim:
            axes.set_xlim(xlim)
        if ylim:
            axes.set_ylim(ylim)

        if label:
            axes.legend(ncols=2,loc="best")

        if title:
            axes.set_title(title)
        return axes
