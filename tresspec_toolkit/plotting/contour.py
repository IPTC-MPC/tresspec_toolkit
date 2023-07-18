import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as mticker
import math
import os
import matplotlib as mpl

from tresspec_toolkit.plotting.config.figure_descriptors import Measurement

# load style specs for custom plot
dir_name = os.path.dirname(os.path.realpath(__file__))
plt.style.use(os.path.join(dir_name, "config/custom.mplstyle"))


def contour(datasets, type_of_measurement=None, time_range=[-np.inf, np.inf], spectral_range=[-np.inf, np.inf],
            cmap='coolwarm', colorbarticks=7, MultipleLocator=None, semilog=False, track_maximum_in_range=None,
            save_figure_to=None, plot_arctan=False):

    """
    :param datasets:               pandas DataFrame containing the data with rows = frequencies, columns = delays
    :param type_of_measurement:    string to specify the type of measurement
    :param time_range:             a list containing the lower and upper limit for delays to be plotted
    :param spectral_range:         a list containing the lower and upper frequencies to trim the plot to
    :param cmap:                   a string specifying the colormap to be used for the plot
    :param colorbarticks:          integer to specify the number of ticks on the color bar
    :param MultipleLocator:        a value to specify the step width of the
    :param semilog:                boolean whether to use log scale
    :param track_maximum_in_range: a list containing the lower and upper bound if on top of the contour representation a
                                   scatter plot is desired that visualizes the shift of the maximum in that range over time
    :param save_figure_to:         the path where to save the figure to if that is desired
    :return:
    """

    if semilog:
        for idx, delay in enumerate(time_range):
            if delay <= 0:
                time_range[idx] = 0.1

    if cmap not in plt.colormaps():
        print('Warning: "', cmap, '" is no valid colormap. Setting colormap to default "seismic" ...')

    if type(colorbarticks) != int:
        print("Warning: invalid number of ticks provided, changing to default (7) ...")

    time_range.sort()
    spectral_range.sort()

    ##########################################################################################################
    #    create an instance of class measurement storing all the relevant descriptions (e.g. axis labels)    #
    ##########################################################################################################
    measurement_flags = Measurement(type_of_measurement)

    # parse data into list if only one dataset is provided so that it can be feed into the subsequent loop over elements
    # of a list
    if not isinstance(datasets, list):
        datasets = [datasets]

    # loop for creation of contour plots
    for measurement in datasets:
        subdata = measurement.iloc[(measurement.index >= min(spectral_range)) &
                                   (measurement.index <= max(spectral_range)),
                                   (measurement.columns >= min(time_range)) &
                                   (measurement.columns <= max(time_range))]

        #################################
        #    Now, creating the plot:    #
        #################################
        norm = mpl.colors.TwoSlopeNorm(0,
                                       vmin=subdata.min().min() if not plot_arctan else np.arctan(subdata.min().min()),
                                       vmax=subdata.max().max() if not plot_arctan else np.arctan(subdata.max().max()))

        # generating ticks on color bar
        abs_max = subdata.abs().to_numpy().max()
        div = math.floor(colorbarticks/2)
        tick = math.floor((abs_max/div)*10)/10 if not plot_arctan else math.floor((np.pi/(2*div))*10)/10

        # creating the plot
        fig, ax = plt.subplots()
        # levels = np.linspace(-abs_max, abs_max, 1000) if not plot_arctan else np.linspace(-np.pi/2, np.pi/2, 1000)
        cf = ax.contourf(subdata.index, subdata.columns,
                         subdata.transpose() if not plot_arctan else np.arctan(subdata.transpose()),
                         levels=1000, cmap=cmap if cmap in plt.colormaps() else 'seismic',
                         norm=norm, extend="both")
        ax.set_xlabel(measurement_flags.xlabel)
        ax.set_ylabel(measurement_flags.ylabel)
        if semilog:
            ax.set_yscale("log")

        #######################################
        #    add scatter plot if requested    #
        #######################################
        if track_maximum_in_range is not None:
            tmp = measurement.iloc[(measurement.index >= min(track_maximum_in_range)) &
                                   (measurement.index <= max(track_maximum_in_range)),
                                   (measurement.columns >= min(time_range)) &
                                   (measurement.columns <= max(time_range))]

            max_frequencies = tmp.idxmax(axis=0)

            ax.autoscale(False)
            ax.scatter(max_frequencies.to_numpy(),
                       max_frequencies.index,
                       zorder=1, facecolors='none', edgecolors="r")

        # adding color bar
        cbar = fig.colorbar(cf, orientation='vertical', extendrect=True,
                            # ticks=mticker.MultipleLocator(MultipleLocator if MultipleLocator is not None else tick),
                            label=measurement_flags.zlabel if not plot_arctan
                            else f"arctan({measurement_flags.zlabel})",
                            ticklocation="left")
        cbar.ax.set_ylabel(measurement_flags.zlabel if not plot_arctan else f"arctan({measurement_flags.zlabel})")

        if save_figure_to is not None:
            manager = plt.get_current_fig_manager()
            manager.resize(*manager.window.maxsize())

            plt.savefig(os.path.join(save_figure_to, "contour_plot.png"),
                        orientation='portrait', transparent=True, bbox_inches="tight", pad_inches=0.1)

    return fig, ax
