import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import numpy as np
import pandas as pd
import os


from tresspec_toolkit.plotting.config.figure_descriptors import Measurement
from tresspec_toolkit.plotting.config.create_colormap import *

import matplotlib
from matplotlib.collections import LineCollection
from matplotlib import colors as mcolors

dirname = os.path.dirname(os.path.realpath(__file__))
plt.style.use(os.path.join(dirname, "config/custom.mplstyle"))


def create_series_of_spectra(data, type_of_measurement=None, time_range=[-np.inf, np.inf],
                             spectral_range=[-np.inf, np.inf], delays_explicit=None, save_figures_to=None,
                             legend_location="best", color_map="viridis", plot_kwargs={}, legend_kwargs={}):

    """
    Invoke to plot transient spectra.

    :param data:                DataFrame containing the data (axis=0: frequency, axis=1: delay)
    :param type_of_measurement: string to specify nature of data
    :param time_range:          array containing lower and upper limit of delays to be shown
    :param spectral_range:      array containing lower and upper limit of frequency/wavelength to be shown
    :param delays_explicit:     array containing delays to be depicted explicitly
    :param save_figures_to:     path where to save the figures to if that is desired
    :param legend_location:     location of the legend box
    :param color_map:           color map used in the plot

    :return:                    a plot of transient spectra
    """

    time_range.sort()
    spectral_range.sort()

    # create an instance of class measurement storing all the relevant descriptions (e.g. axis labels)

    measurement_flags = Measurement(type_of_measurement)

    if type(data) != list:
        data = [data]

    subdata = list()

    # compile data to be plotted
    if not delays_explicit:
        # use the provided time range and spectral range to trim the data if desired
        for measurement in range(len(data)):
            tmp = data[measurement].iloc[
                (data[measurement].index >= min(spectral_range)) & (data[measurement].index <= max(spectral_range)),
                (data[measurement].columns >= min(time_range)) & (data[measurement].columns <= max(time_range))]
            subdata.append(tmp)
    else:
        print('Delays defined explicitly: ', delays_explicit)
        for measurement in range(len(data)):
            tmp = list()
            for delay in delays_explicit:
                tmp0 = data[measurement].iloc[(data[measurement].index >= min(spectral_range)) &
                                              (data[measurement].index <= max(spectral_range)),
                                              abs(data[measurement].columns - delay) ==
                                              min(abs(data[measurement].columns - delay))]
                tmp.append(tmp0)

            subdata.append(pd.concat(tmp, axis=1))

    # plot spectra
    for measurement in subdata:
        no_delays = len(measurement.columns)

        #    creating color map to be used subsequently    #
        cmap, _ = create_colormap(color_map, no_delays)

        if type_of_measurement == "UVmIR":
            labels = [f"{delay} ps" if delay < 1000 else
                      f"{round(delay/1000, 1)} ns" if 1000 <= delay < 1e6 else
                      f"{round(delay/1e6, 1)} $\mu$s"
                      for delay in measurement.columns]
        else:
            labels = [f"{delay} {measurement_flags.timescale}" for delay in measurement.columns]


        for idx in range(no_delays):

            fig, ax = plt.subplots(figsize=(23.5, 13.2))
            for idx2, delay in enumerate(measurement.columns[:idx+1]):
                ax.plot(measurement.index, measurement.loc[:, delay],
                        label=str(delay) + " " + measurement_flags.timescale, color=cmap[idx2])
            ax.set_xlabel(measurement_flags.xlabel)
            ax.set_ylabel(measurement_flags.zlabel)
            # ax.legend(ncol=2, loc=legend_location, labelcolor="linecolor", handlelength=0.0)
            ax.legend(labels, **legend_kwargs)

            if save_figures_to is not None:
                # manager = plt.get_current_fig_manager()
                # manager.resize(*manager.window.maxsize())

                plt.savefig(os.path.join(save_figures_to,
                                         "up_to_" + str(measurement.columns[idx]) +
                                         measurement_flags.timescale + ".png"),
                            facecolor="w", edgecolor="b", orientation="portrait", transparent=True,
                            bbox_inches="tight", pad_inches=0.1)
