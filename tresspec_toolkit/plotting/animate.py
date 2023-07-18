import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

from tresspec_toolkit.plotting.config.figure_descriptors import Measurement


def animate(data, type_of_measurement=None):

    """
    Function to create an animation of time-resolved spectra
    :param data:
    :param type_of_measurement:
    :return:
    """


    measurement_flags = Measurement(type_of_measurement)


    fig, ax = plt.subplots()
    ax = plt.axes(xlim=(min(data.index), max(data.index)),
                  ylim=(1.1 * np.min(data.to_numpy()), 1.1 * np.max(data.to_numpy())))
    ax.set_xlabel(measurement_flags.xlabel)
    ax.set_ylabel(measurement_flags.zlabel)
    line, = ax.plot([], [], lw=2)

    # line.set_label([])
    # ax2.legend()

    def init():
        line.set_data([], [])
        return line,

    def animate_data(i):
        x1 = data.index
        y1 = data.iloc[:, i]
        line.set_data(x1, y1)
        # line.set_label(f"{i} ps")
        return line,

    #anim = animation.FuncAnimation(fig, animate_data, init_func=init,
    #                               frames=data.shape[1], interval=100, blit=True)

    animation.FuncAnimation(fig, animate_data, init_func=init,
                                   frames=data.shape[1], interval=100, blit=True)

    plt.show()
#    return anim
