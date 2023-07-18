import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import copy
from scipy.stats import median_abs_deviation
from scipy.signal import correlate2d


def cross_correlate_runs(datasets, plot=True):

    cross_correlations = list()
    nd = len(datasets)          # number of data sets

    for data1 in datasets:
        cc = list()
        for data2 in datasets:
            cc.append(correlate2d(data1.to_numpy(), data2.to_numpy(), mode="full", boundary="symm"))
        cross_correlations.append(cc)

    # make figures
    if plot:
        # figure of runs (each separately)
        fig, ax = plt.subplots(1, nd, figsize=(nd * 4, 4), sharey=True)
        for idx, data in enumerate(datasets):

            ax[idx].set_title("Run " + str(idx+1))

            levels = np.linspace(-data.abs().to_numpy().max(), data.abs().to_numpy().max(), 1000)
            ax[idx].contourf(data.index, data.columns, data.T, levels=levels, cmap="seismic")

        ########################################
        # make figures of cross correlations
        fig, ax = plt.subplots(nd, nd, figsize=(2 * nd, 2 * nd), sharex=True, sharey=True)

        for idx1, cc in enumerate(cross_correlations):
            for idx2, cc2 in enumerate(cc):

                levels = np.linspace(-cc2.max(), cc2.max(), 1000)
        #        ax[idx1, idx2].contourf(np.arange(0, len(cc2)) + 1 - (len(cc2) + 1)/2,
        #                                np.arange(0, len(cc2)) + 1 - (len(cc2) + 1)/2, cc2.T,
        #                                levels=levels, cmap="seismic")

                ax[idx1, idx2].contourf(np.arange(0, cc2.shape[0]),
                                        np.arange(0, cc2.shape[1]), cc2.T,
                                        levels=levels, cmap="seismic")


    #  + 1 - len(cc2)  + 1 - len(cc2)
    #y, x = np.unravel_index(np.argmax(cc), cc.shape)  # find the match
    #print((y +1)- Size, (x+1) - Size)

    #
    #
    # cc = correlate2d(dummy_data1, dummy_data2, mode="full")
    # cross_correlation = pd.DataFrame(cc, index=np.arange(0, cc.shape[0]), columns=np.arange(0, cc.shape[1]))
    #
    #
    # # make figures
    # fig, ax = plt.subplots(1, 3, figsize=(18, 6), sharey=False)
    #
    # ax[0].set_title("Data 1")
    # ax[1].set_title("Data 2")
    # ax[2].set_title("Cross Correlation")
    #
    #
    # levels = np.linspace(-dummy_data1.abs().to_numpy().max(), dummy_data1.abs().to_numpy().max(), 1000)
    # ax[0].contourf(dummy_data1.index, dummy_data1.columns, dummy_data1.T, levels=levels, cmap="seismic")
    #
    # levels = np.linspace(-dummy_data2.abs().to_numpy().max(), dummy_data2.abs().to_numpy().max(), 1000)
    # ax[1].contourf(dummy_data2.index, dummy_data2.columns, dummy_data2.T, levels=levels, cmap="seismic")
    #
    # levels = np.linspace(-cross_correlation.abs().to_numpy().max(), cross_correlation.abs().to_numpy().max(), 1000)
    # ax[2].contourf(cross_correlation.index, cross_correlation.columns, cross_correlation.T, levels=levels, cmap="seismic")
    #
    #
    # y, x = np.unravel_index(np.argmax(cc), cc.shape)  # find the match
    # print((y +1)- Size, (x+1) - Size)