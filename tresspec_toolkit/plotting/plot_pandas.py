import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tresspec_toolkit.plotting.config.figure_descriptors import Measurement
from tresspec_toolkit.plotting.config.create_colormap import *


def plot_pandas(data, type_of_measurement=None, time_range=[-np.inf, np.inf], color_map="viridis inverted",
                legend_loc="best", spectral_range=[None, None]):

    time_range.sort()

    measurement_flags = Measurement(type_of_measurement)


    if type(data) != list:
        data = [data]

    for measurement in data:
        number_of_delays = measurement.iloc[:, (measurement.columns >= min(time_range)) &
                                               (measurement.columns <= max(time_range))].shape[1]


        _, colors = create_colormap(color_map, number_of_delays)
        fig, ax = plt.subplots()

        measurement.plot(y=measurement.columns[(measurement.columns >= min(time_range)) &
                                               (measurement.columns <= max(time_range))],
                         xlabel=measurement_flags.xlabel,
                         ylabel=measurement_flags.zlabel,
                         colormap=colors, ax=ax,
                         xlim=spectral_range)

        ax.legend([f"{i} {measurement_flags.timescale}"
                   for i in measurement.columns[(measurement.columns >= min(time_range)) &
                                                (measurement.columns <= max(time_range))]], ncol=2,
                  loc=legend_loc)
        #    creating color map to be used subsequently    #

        #
        # fig, ax = plt.subplots()
        # ax.set_prop_cycle(color=[color for color in colors])
        # ax.plot(measurement.index, measurement)
        # ax.set_xlabel(measurement_flags.xlabel)
        # ax.set_ylabel(measurement_flags.zlabel)
        # ax.legend([str(i) + " " + measurement_flags.timescale for i in measurement.columns], ncol=2,
        #           loc=legend_loc)

