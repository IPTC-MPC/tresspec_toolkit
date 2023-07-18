import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from tresspec_toolkit.plotting.config.figure_descriptors import Measurement
from tresspec_toolkit.plotting.config.create_colormap import *

# load style specs for custom plot
dir_name = os.path.dirname(os.path.realpath(__file__))
plt.style.use(os.path.join(dir_name, "config/custom.mplstyle"))


def kinetic_traces(data, type_of_measurement=None, take_traces_at=None, separate_plots=False, semilog=False,
                   color_map="viridis inverted", fitting_results=None, time_range=[-np.inf, np.inf],
                   plot_kwargs={}, legend_kwargs={}):

    """

    :param data:                the data as a pandas DataFrame or a list thereof
    :param type_of_measurement: a string specifying the nature of the measurement
    :param take_traces_at:      a list containing the spectral positions where to take transients (optional, otherwise a
                                transient trace at every single spectral position is plotted)
    :param separate_plots:      boolean whether to create a separate plot for each individual frequency
    :param semilog:             boolean whether to plot the transient trace in a semi-logarithmic fashion wrt. the delay
    :param color_map:           the underlying color map specifying the coloring of the plot(s)
    :param fitting_results:     an instance of the FitResults class to simultaneously plot (optional)
    :return:
    """

    # create class object storing axes descriptions
    measurement_flags = Measurement(type_of_measurement)

    if type(data) != list:
        data = [data]

    subdata = list()
    for measurement in data:
        if take_traces_at is None:
            subdata.append(measurement)
        else:
            tmp = list()
            for frequency in take_traces_at:
                tmp0 = measurement.iloc[abs(measurement.index - frequency)
                                        == min(abs(measurement.index - frequency)),
                                        (measurement.columns >= min(time_range)) &
                                        (measurement.columns <= max(time_range))]
                tmp.append(tmp0)
            subdata.append(pd.concat(tmp, axis=0).sort_index())

    #####################
    #    making plot    #
    #####################
    for measurement in subdata:
        wn, _ = measurement.shape

        colors, _ = create_colormap(color_map, wn)

        if not separate_plots:
            fig, ax = plt.subplots()
            ax.set_prop_cycle(color=[color for color in colors])
            if semilog:
                ax.semilogx(measurement.columns, measurement.to_numpy().transpose(),
                            marker="o", linestyle="None")
            else:
                ax.plot(measurement.columns, measurement.to_numpy().transpose(),
                        marker="o", linestyle="None", **plot_kwargs)

            ax.set_xlabel(measurement_flags.ylabel)
            ax.set_ylabel(measurement_flags.zlabel)
            ax.legend([str(int(round(wn, 0))) + " " + measurement_flags.energyunit for wn in measurement.index],
                      **legend_kwargs)
            ax.axhline(color="k", alpha=0.2)
        else:
            for wn in measurement.index:
                fig, ax = plt.subplots()
                ax.scatter(measurement.columns, measurement.loc[wn, :],
                           label=str(int(round(wn, 0))) + " " + measurement_flags.energyunit, color=colors[-1])

                ax.set_xlabel(measurement_flags.ylabel)
                ax.set_ylabel(measurement_flags.zlabel)
                ax.legend()
                ax.axhline(color="k", alpha=0.2)
