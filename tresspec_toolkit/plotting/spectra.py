import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import numpy as np
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import pandas as pd
import os


from tresspec_toolkit.plotting.config.figure_descriptors import Measurement
from tresspec_toolkit.plotting.config.create_colormap import *


import matplotlib
from matplotlib.collections import LineCollection
from matplotlib import colors as mcolors

dirname = os.path.dirname(os.path.realpath(__file__))
plt.style.use(os.path.join(dirname, "config/custom.mplstyle"))


def spectra(data, type_of_measurement=None, time_range=[-np.inf, np.inf], spectral_range=[-np.inf, np.inf],
            delays_explicit=None, color_map="viridis inverted", legend_loc="best", plot_kwargs={}, legend_kwargs={},
            title=None):

    """
    Invoke to plot transient spectra.

    :param data:                DataFrame containing the data (axis=0: frequency, axis=1: delay)
    :param type_of_measurement: string to specify nature of data
                                ("uv-pump-mir-probe", "uv-pump-vis-probe", "step-scan", "rapid-scan",
                                "IR series")
    :param time_range:          array containing lower and upper limit of delays to be shown
    :param spectral_range:      array containing lower and upper limit of frequency/wavelength to be shown
    :param delays_explicit:     array containing delays to be depicted explicitly
    :param color_map:           the colormap used for the plot (defaults to "viridis inverted")
    :param legend_loc:          specifier for location of legend
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
    if delays_explicit is not None:
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
    else:
        # use the provided time range and spectral range to trim the data if desired
        for measurement in range(len(data)):
            tmp = data[measurement].iloc[
                (data[measurement].index >= min(spectral_range)) & (data[measurement].index <= max(spectral_range)),
                (data[measurement].columns >= min(time_range)) & (data[measurement].columns <= max(time_range))]
            subdata.append(tmp)

    # plot spectra
    for measurement in subdata:
        delays = measurement.columns

        #    creating color map to be used subsequently    #
        colors, _ = create_colormap(color_map, len(delays))

        if measurement_flags.type_of_measurement == "UV-pump mIR-probe":
            labels = [f"{delay} ps" if delay < 1000 else
                      f"{round(delay / 1000, 1)} ns" if 1000 <= delay < 1e6 else
                      f"{round(delay / 1e6, 1)} $\mathregular{{\mu}}$s"
                      for delay in measurement.columns]
        else:
            labels = [f"{delay} {measurement_flags.timescale}" for delay in measurement.columns]

        ################################################################################################################
        # now, let's actually make the figure
        fig, ax = plt.subplots()
        if title is not None:
            ax.set_title(title)

        ax.set_prop_cycle(color=[color for color in colors])

        ax.plot(measurement.index, measurement, **plot_kwargs)
        ax.set_xlabel(measurement_flags.xlabel)
        ax.set_ylabel(measurement_flags.zlabel)
        ax.legend(labels, **legend_kwargs)
        ax.axhline(color="k", alpha=0.2)
        ################################################################################################################
