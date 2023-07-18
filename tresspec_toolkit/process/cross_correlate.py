import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import copy
from scipy.signal import fftconvolve


def cross_correlate(datasets, plot=True, cmap=None):

    """

    :param datasets:
    :param plot:
    :param cmap:
    :return:
    """

    if cmap is None:
        cmap = "viridis"

    cross_correlations = list()
    nd = len(datasets)          # number of data sets

    # calculate cross correlations by convolution with rotated image
    for data1 in datasets:
        cc = list()
        for data2 in datasets:
            cc.append(fftconvolve(data1.to_numpy(), data2.to_numpy()[::-1, ::-1], mode="same"))
        cross_correlations.append(cc)

    # make figures
    if plot:
        # figure of runs (each separately)
        fig, ax = plt.subplots(1, nd, figsize=(nd * 4, 4), sharey=True)
        for idx, data in enumerate(datasets):

            ax[idx].set_title("Run " + str(idx+1))

            levels = np.linspace(-data.abs().to_numpy().max(), data.abs().to_numpy().max(), 1000)
            ax[idx].contourf(data.index, data.columns, data.T, levels=levels, cmap="seismic")

        ############################################
        #    make figures of cross correlations    #
        ############################################
        fig, ax = plt.subplots(nd, nd, figsize=(2 * nd, 2 * nd), sharex=True, sharey=True)

        for idx1, cc in enumerate(cross_correlations):
            for idx2, cc2 in enumerate(cc):

                levels = np.linspace(-cc2.max(), cc2.max(), 1000)
        #        ax[idx1, idx2].contourf(np.arange(0, len(cc2)) + 1 - (len(cc2) + 1)/2,
        #                                np.arange(0, len(cc2)) + 1 - (len(cc2) + 1)/2, cc2.T,
        #                                levels=levels, cmap="seismic")

                #ax[idx1, idx2].contourf(np.arange(0, cc2.shape[0]),
                #                        np.arange(0, cc2.shape[1]), cc2.T,
                #                        levels=levels, cmap="seismic")

                ax[idx1, idx2].imshow(cc2, cmap=cmap)

                y, x = np.unravel_index(np.argmax(cc2), cc2.shape)  # find the match

                ax[idx1, idx2].plot(x, y, 'go')
                #ax[idx1, idx2].text(x, y+5, "x = " + str(x) + ";\ny = " + str(y), fontsize=10, color="g")

                ax[idx1, idx2].axes.xaxis.set_visible(False)
                ax[idx1, idx2].axes.yaxis.set_visible(False)

        fig.subplots_adjust(wspace=0, hspace=0)

        manager = plt.get_current_fig_manager()
        manager.resize(*manager.window.maxsize())
