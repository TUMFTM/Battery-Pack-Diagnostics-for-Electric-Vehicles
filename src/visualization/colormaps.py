# https://towardsdatascience.com/creating-colormaps-in-matplotlib-4d4de78a04b8
import numpy as np
from matplotlib.colors import ListedColormap
from src.visualization.config_visualization import VisualizationConfig

class ColorMaps():

    def __init__(self):
        pass

    @staticmethod
    def blue_orange_tum(grayscale=0.5):

        N = 256
        # create blue colormap
        blue = np.ones((N, 4))
        blue[:, 0] = np.linspace(VisualizationConfig.TUMblau.value[0], grayscale, N) # 0.5 makes the middle part gray
        blue[:, 1] = np.linspace(VisualizationConfig.TUMblau.value[1], grayscale, N) # 1 would make it white
        blue[:, 2] = np.linspace(VisualizationConfig.TUMblau.value[2], grayscale, N)
        blue_cmp = ListedColormap(blue)

        # create orange colormap
        orange = np.ones((N, 4))
        orange[:, 0] = np.linspace(VisualizationConfig.TUMorange.value[0], grayscale, N)
        orange[:, 1] = np.linspace(VisualizationConfig.TUMorange.value[1], grayscale, N)
        orange[:, 2] = np.linspace(VisualizationConfig.TUMorange.value[2], grayscale, N)
        orange_cmp = ListedColormap(orange)

        new_cmap = np.vstack((blue_cmp(np.linspace(0, 1, 128)),
                                orange_cmp(np.linspace(1, 0, 128))))
        tum_orange_blue = ListedColormap(new_cmap, name='tum_orange_blue')
        return tum_orange_blue

    @staticmethod
    def blue_tum():
        N = 256
        # create blue colormap
        blue = np.ones((N, 4))
        blue[:, 0] = np.linspace(VisualizationConfig.TUMblau.value[0], 0.9, N)  # 0.9 makes the middle part light gray
        blue[:, 1] = np.linspace(VisualizationConfig.TUMblau.value[1], 0.9, N)  # 1 would make it white
        blue[:, 2] = np.linspace(VisualizationConfig.TUMblau.value[2], 0.9, N)
        blue_cmp = ListedColormap(blue,name='tum_blue')
        return blue_cmp

    @staticmethod
    def orange_tum():
        N = 256
        # create orange colormap
        orange = np.ones((N, 4))
        orange[:, 0] = np.linspace(VisualizationConfig.TUMorange.value[0], 0.9, N)  # 0.9 makes the middle part light gray
        orange[:, 1] = np.linspace(VisualizationConfig.TUMorange.value[1], 0.9, N)  # 1 would make it white
        orange[:, 2] = np.linspace(VisualizationConfig.TUMorange.value[2], 0.9, N)
        orange_cmp = ListedColormap(orange,name='tum_orange')
        return orange_cmp