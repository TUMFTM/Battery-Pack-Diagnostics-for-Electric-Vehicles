from src.visualization.config_visualization import VisualizationConfig
import matplotlib.pyplot as plt
from src.voltage_capacity_analysis.vca_base import VCABase

class VisualizeEVS(VCABase):
    """
    create the EVS Plots
    """
    def __init__(self):
        super(VisualizeEVS, self).__init__()

    def DVA_plot(self,capacity, dva, normalized=True,axes=None, label=None, linestyle="-", xlim=None, ylim=None, **kwargs):
        if not axes:
            _, axes = plt.subplots(1, 1,
                                 figsize=(VisualizationConfig.col_width_two_col_doc_in_inch.value,  # width
                                          VisualizationConfig.height.value))  # heigth

        axes.plot(capacity,dva, linestyle, label=label, **kwargs)
        axes.grid(color="gainsboro")
        axes.set_axisbelow(True)
        axes.set_xlabel('capacity in Ah')

        if normalized:
            axes.set_ylabel("DVA in V")
        else:
            axes.set_ylabel("DVA in V/Ah")

        if xlim:
            axes.set_xlim(xlim)
        if ylim:
            axes.set_ylim(ylim)

        if label:
            axes.legend(ncols=2,loc="upper right")
        return axes

    def ICA_plot(self, voltage, ica, axes=None, label=None, linestyle="-", xlim=None, ylim=None,
                 **kwargs):
        if not axes:
            _, axes = plt.subplots(1, 1,
                                   figsize=(VisualizationConfig.col_width_two_col_doc_in_inch.value,  # width
                                            VisualizationConfig.height.value))  # heigth

        axes.plot(voltage, ica, linestyle, label=label, **kwargs)
        axes.grid(color="gainsboro")
        axes.set_axisbelow(True)
        axes.set_xlabel('voltage in V')
        axes.set_ylabel("ICA in Ah/V")


        if xlim:
            axes.set_xlim(xlim)
        if ylim:
            axes.set_ylim(ylim)

        if label:
            axes.legend(ncols=2, loc="upper right")
        return axes

    def EVS_plot(self,capacity, dva, voltage,ica,axes=None, label=None, linestyle="-",ylim_dva=None,ylim_ica=None, **kwargs):
        NoneType = type(None)
        if isinstance(axes, NoneType):
            fig, axes = plt.subplots(1, 2,
                                 figsize=(VisualizationConfig.col_width_two_col_doc_in_inch.value*2,  # width
                                          VisualizationConfig.height.value))  # heigth

        self.DVA_plot(capacity, dva, normalized=True,axes=axes[0], label=None, linestyle=linestyle, xlim=None, ylim=ylim_dva, **kwargs)
        self.ICA_plot(voltage, ica, axes=axes[1], label=label, linestyle=linestyle, xlim=None, ylim=ylim_ica,**kwargs)

        return axes