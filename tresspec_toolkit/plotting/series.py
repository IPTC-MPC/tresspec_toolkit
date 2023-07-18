import matplotlib.pyplot as plt
from tresspec_toolkit.plotting.config.create_colormap import *
from tresspec_toolkit.process.extract_selected_delays import *
from tresspec_toolkit.plotting.config.figure_descriptors import Measurement
import os


def series(dod, type_of_measurement=None, dirname=None, show_vline_at=None, delays=None,
           y_limits=None, x_limits=None, zero_hline=True, legend_location="best", legend_ncol=2):

    """
    A function that is used to create plots of consecutive pump-probe spectra to visualize the evolution of the signals
    (for example to be used as an animation in a PowerPoint presentation)
    :param dod:
    :param type_of_measurement:
    :param dirname:
    :param show_vline_at:
    :param delays:
    :param y_limits:
    :param x_limits:
    :param zero_hline:
    :param legend_location:
    :param legend_ncol:
    :return:
    """

    descriptors = Measurement(type_of_measurement)

    if delays is not None:
        dod = extract_selected_delays(dod, delays=delays)

    _, no_delays = dod.shape
    colors = create_colormap("VibrationalCooling", no_delays)

    def return_y_limits(data):
        y0 = data.to_numpy().min()
        y1 = data.to_numpy().max()

        delta = y1 - y0
        decimals = int(np.floor(np.log10(delta)) - 1)
        factor = 10 ** decimals

        y0 = np.floor(y0 / factor) * factor
        y1 = np.ceil(y1 / factor) * factor

        return y0, y1

    # initialize limits for y-axis
    if y_limits is None:
        y_min, y_max = return_y_limits(dod)
        print(f"Automatically chosen limits for y-axis: [{y_min}; {y_max}]")
    else:
        y_min = min(y_limits)
        y_max = max(y_limits)

    # initialize limits for x-axis
    if x_limits is None:
        x_min = np.ceil(min(dod.index))
        x_max = np.ceil(max(dod.index))
    else:
        x_min = min(x_limits)
        x_max = max(x_limits)
        print(f"x_min = {x_min}; x_max = {x_max}")

    #############################################
    #    loop over delays and create figures    #
    #############################################
    for idx, delay in enumerate(dod.columns):

        #if show_vline_at is not None and delay == show_vline_at
        #if delay == 20.0:
        #    show_vline = True

        fig, ax = plt.subplots()

        # creating color map
        colors, _ = create_colormap("VibrationalCooling", no_delays)
        for i in range(idx):
            colors[i, -1] = 0.25

        # setting colormap
        ax.set_prop_cycle(color=[color for color in colors])

        # creating plot
        ax.plot(dod.index, dod.loc[:, :delay])
        ax.set_xlim(xmin=x_min, xmax=x_max)
        ax.set_ylim(ymin=y_min, ymax=y_max)

        ax.set_xlabel(descriptors.xlabel)
        ax.set_ylabel(descriptors.zlabel)

        if zero_hline:
            ax.axhline(0.0, linestyle='-', color='k', alpha=0.2)  # horizontal line

        # adding vertical line for delays of 20 ps and onwards

        if show_vline_at is not None:
            if delay >= show_vline_at[1]:
                ax.axvline(show_vline_at[0], linestyle='--', color='k', alpha=0.2)  # vertical line

        ax.legend([str(tau) + " ps" for tau in dod.columns[:idx + 1]], ncol=legend_ncol, loc=legend_location,
                  frameon=False)

        manager = plt.get_current_fig_manager()
        manager.resize(*manager.window.maxsize())

        figure_filename = os.path.join(dirname, f"up_to_{delay}_{descriptors.timescale}.png")


        # figure_filename = \
        #    \FTIR_spectrum_epsilon_complete.png"

        plt.savefig(figure_filename, orientation='portrait', transparent=True, bbox_inches="tight", pad_inches=0.1)
