import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm

from tresspec_toolkit.plotting.config.colormaps import *


def create_colormap(cmap, no_traces):


    if cmap in plt.colormaps():
        print("Found default color map")
        colors = cm.get_cmap(cmap, no_traces)
    else:
        if cmap.lower() in ["vibrationalcooling", "vibrational cooling"]:
            vals = np.ones((no_traces, 4))
            vals[:, 0] = np.linspace(0.8, 0, no_traces)  # Red
            vals[:, 1] = np.linspace(0.2, 0.3, no_traces)  # Green
            vals[:, 2] = np.linspace(0, 1, no_traces)  # Blue
            colors = ListedColormap(vals, name="VibrationalCooling")
        elif cmap.lower() in ["vibrationalcoolinginverted", "vibrational cooling inverted"]:
            vals = np.ones((no_traces, 4))
            vals[:, 2] = np.linspace(0.8, 0, no_traces)  # Red
            vals[:, 1] = np.linspace(0.2, 0.3, no_traces)  # Green
            vals[:, 0] = np.linspace(0, 1, no_traces)  # Blue
            colors = ListedColormap(vals, name="VibrationalCooling")
        elif cmap == "parula":
            new_cmp = parula()
        # elif cmap == "inferno":
        #    new_cmp = inferno(no_traces)
        else:                                                       # "viridis inverted"
            colors = cm.get_cmap("viridis", no_traces)
            colors.colors = np.flipud(colors.colors)

    color_map = colors(range(no_traces))

    return color_map, colors
