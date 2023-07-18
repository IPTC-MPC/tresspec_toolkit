import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib
# load style specs for custom plot
import os

from tresspec_toolkit.plotting.config.figure_descriptors import Measurement
from tresspec_toolkit.plotting.config.create_colormap import *
from tresspec_toolkit.analyze.fitfunctions import *


dirname = os.path.dirname(os.path.realpath(__file__))
plt.style.use(os.path.join(dirname, "config/custom.mplstyle"))


def kinetic_traces_and_fits(data, type_of_measurement=None, offsets=None, legend_location=None, separate_plots=False,
                            semilog=False, color_map="viridis inverted", save_figures_to=None, frame_on=True):

    """
    invoke kinetic traces and fits is used to prepare plots of kinetic traces and there respective fits.

    :param data:                an object of the fits class as returned from the function "fitting"
    :param type_of_measurement: a string to specify the type of measurement in order to set labels etc.
    :param offsets:             boolean whether to offset the respective datasets for clarity
    :param legend_location:     where to place the legend
    :param separate_plots:      boolean whether to create a separate plot for each trace
    :param semilog:             boolean whether to plot the data in a semilogarithmic fashion (logarithmic delay axis)
    :param color_map:           string specifying which color map to use for the plot
    :param save_figures_to:     a path where to save the figure(s) to if that is desired
    :param frame_on:            boolean whether to draw a frame around the legend box
    :return:
    """

    # create class object storing axes descriptons
    measurement_flags = Measurement(type_of_measurement)

    no_traces = len(data)

    if offsets is None:
        offsets = np.zeros(no_traces)

    # creating a colormap
    colors, _ = create_colormap(color_map, no_traces)

    ##################
    #    plotting    #
    ##################
    if separate_plots:               # creating separate plot (one for each kinetic trace)
        for idx, key in enumerate(data):
            fig, ax = plt.subplots()
            ax.plot(data[key].x, data[key].y + offsets[idx], marker="o", linestyle="None",
                    color=colors[-1],
                    label=str(int(round(float(key), 0))) + " " + measurement_flags.energyunit, )
            ax.plot(data[key].x, data[key].fitted_curve + offsets[idx], color=colors[-1])

            ax.set_xlabel(measurement_flags.ylabel)
            ax.set_ylabel(measurement_flags.zlabel)
            ax.set_xscale("log" if semilog else "linear")
            ax.legend(loc="best" if legend_location is not None else legend_location)
    else:                           # pasting all into one plot
        fig, ax = plt.subplots()
        for idx, key in enumerate(data):
            ax.plot(data[key].x, data[key].y + offsets[idx], marker="o", linestyle="None",
                    color=colors[idx],
                    label=str(int(round(float(key), 0))) + " " + measurement_flags.energyunit,)
            ax.plot(data[key].x, data[key].fitted_curve + offsets[idx], color=colors[idx])

        ax.set_xlabel(measurement_flags.ylabel)
        ax.set_ylabel(measurement_flags.zlabel)
        ax.set_xscale("log" if semilog else "linear")

        ax.legend(loc="best" if legend_location is None else legend_location, frameon=frame_on)

        if save_figures_to is not None:
            manager = plt.get_current_fig_manager()
            manager.resize(*manager.window.maxsize())

            plt.savefig(os.path.join(save_figures_to, "kinetic_traces_and_fits.png"),
                        orientation='portrait', transparent=True, bbox_inches="tight", pad_inches=0.1)

    return fig, ax
