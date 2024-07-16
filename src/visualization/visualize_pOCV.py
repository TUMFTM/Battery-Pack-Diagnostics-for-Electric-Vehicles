from src.visualization.config_visualization import VisualizationConfig
import matplotlib.pyplot as plt
from src.voltage_capacity_analysis.vca_base import VCABase

class VisualizepOCV(VCABase):
    """
    create the pOCV Plot
    """
    def __init__(self):
        super(VisualizepOCV, self).__init__()

    def pOCV_plot(self,time, current, voltage,axes=None, label=None, linestyle="-", xlim=None, ylim=None, **kwargs):
        if not axes:
            _, axes = plt.subplots(1, 1,
                                 figsize=(VisualizationConfig.columnwidth_in_in.value,  # width
                                          VisualizationConfig.columnwidth_in_in.value))  # heigth

        charge = self.calculate_capacity_signal(time,current,initial=0)
        axes.plot(charge,voltage, linestyle, label=label, **kwargs)
        axes.grid(color="gainsboro")
        axes.set_axisbelow(True)
        axes.set_xlabel('charge in Ah')
        axes.set_ylabel("voltage in V")

        if xlim:
            axes.set_xlim(xlim)
        if ylim:
            axes.set_ylim(ylim)

        if label:
            axes.legend(ncols=1,loc="lower right")
        return axes

    def current_plot(self,time, current, axes=None, label=None, linestyle="-", xlim=None, ylim=None, **kwargs):
        if not axes:
            _, axes = plt.subplots(1, 1,
                                 figsize=(VisualizationConfig.columnwidth_in_in.value,  # width
                                          VisualizationConfig.columnwidth_in_in.value))  # heigth

        axes.plot(time,current, linestyle, label=label, **kwargs)
        axes.grid(color="gainsboro")
        axes.set_axisbelow(True)
        axes.set_xlabel('time in hours')
        axes.set_ylabel("current in A")
        axes.ticklabel_format(useOffset=False)

        if xlim:
            axes.set_xlim(xlim)
        if ylim:
            axes.set_ylim(ylim)

        if label:
            axes.legend(ncols=2,loc="lower right")
        return axes

    def charge_plot(self,time, current, axes=None, label=None, linestyle="-", xlim=None, ylim=None, **kwargs):
        if not axes:
            _, axes = plt.subplots(1, 1,
                                 figsize=(VisualizationConfig.columnwidth_in_in.value,  # width
                                          VisualizationConfig.columnwidth_in_in.value))  # heigth
        charge = self.calculate_capacity_signal(time, current, initial=0)
        axes.plot(time,charge, linestyle, label=label, **kwargs)
        axes.grid(color="gainsboro")
        axes.set_axisbelow(True)
        axes.set_xlabel('time in hours')
        axes.set_ylabel("charge in Ah")

        if xlim:
            axes.set_xlim(xlim)
        if ylim:
            axes.set_ylim(ylim)

        if label:
            axes.legend(ncols=2,loc="lower right")
        return axes

    def voltage_plot(self, time, voltage, axes=None, label=None, linestyle="-", xlim=None, ylim=None, **kwargs):
        if not axes:
            _, axes = plt.subplots(1, 1,
                                   figsize=(VisualizationConfig.columnwidth_in_in.value,  # width
                                            VisualizationConfig.columnwidth_in_in.value))  # heigth

        axes.plot(time, voltage, linestyle, label=label, **kwargs)
        axes.grid(color="gainsboro")
        axes.set_axisbelow(True)
        axes.set_xlabel('time in hours')
        axes.set_ylabel("voltage in V")

        if xlim:
            axes.set_xlim(xlim)
        if ylim:
            axes.set_ylim(ylim)

        if label:
            axes.legend(ncols=2, loc="lower right")
        return axes

    def pOCV_voltage_current_charge_plot(self,time, current, voltage,axes=None, label=None, linestyle="-", **kwargs):
        NoneType = type(None)
        if isinstance(axes, NoneType):
            fig, axes = plt.subplots(2, 2,
                                 figsize=(VisualizationConfig.textwidth_in_in.value,  # width
                                          VisualizationConfig.textwidth_in_in.value))  # heigth
            plt.subplots_adjust(left=0.1,
                                bottom=0.1,
                                right=0.9,
                                top=0.9,
                                wspace=0.25,
                                hspace=0.25)

        self.pOCV_plot(time, current, voltage,axes=axes[0][0], label=label, linestyle=linestyle, **kwargs)
        self.voltage_plot(time, voltage, axes=axes[0][1], linestyle=linestyle, **kwargs)
        self.charge_plot(time, current, axes=axes[1][0], linestyle=linestyle, **kwargs)
        self.current_plot(time, current, axes=axes[1][1], linestyle=linestyle, **kwargs)

        return axes

    def pOCV_voltage_current_plot(self,time, current, voltage,axes=None, label=None, linestyle="-", **kwargs):
        NoneType = type(None)
        if isinstance(axes, NoneType):
            fig, axes = plt.subplots(1, 2,
                                 figsize=(VisualizationConfig.textwidth_in_in.value,  # width
                                          VisualizationConfig.columnwidth_in_in.value))  # heigth
            plt.subplots_adjust(left=0.1,
                                bottom=0.1,
                                right=0.9,
                                top=0.9,
                                wspace=0.25,
                                hspace=0.25)

        self.voltage_plot(time, voltage, axes=axes[0], linestyle=linestyle, label=label, **kwargs)
        self.current_plot(time, current, axes=axes[1], linestyle=linestyle, label=label, **kwargs)
        return axes