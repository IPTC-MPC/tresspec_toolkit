import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def subtractsignalsfrombeforezero(datasets, tau=-2, plot=False):
    """

    :param datasets: the data as a pandas DataFrame or a list thereof
    :param tau:      an upper limit or a list specifying the time interval to determine the signal that occurs before t0
    :return:         the data from which the residual signal has been subtracted
    """

    if type(tau) != list:
        tau = [-np.inf, tau]

    if type(datasets) != list:
        datasets = [datasets]

    subdata = list()
    for data in datasets:

        av_0 = data.iloc[:, (data.columns >= min(tau)) & (data.columns <= max(tau))].mean(axis=1)
        # av_0 = data.iloc[:, (data.columns >= min(tau)) & (data.columns <= max(tau))].median(axis=1)

        no_wn, no_delays = data.shape

        # parse into dataframe
        baseline = pd.DataFrame(np.tile(av_0.to_numpy().reshape(no_wn, 1), no_delays), index=data.index, columns=data.columns)

        subdata.append(data - baseline)

        # make plots if that is desired to kee track of the things the function does
        if plot:
            fig, ax = plt.subplots(3, 1, sharex=True)
            plt.subplots_adjust(hspace=0.0)
            ax[0].plot(data.index, data.iloc[:, (data.columns >= min(tau)) & (data.columns <= max(tau))])
            ax[1].plot(av_0)
            ax[2].plot(subdata[-1].index, subdata[-1].iloc[:, (data.columns >= min(tau)) & (data.columns <= max(tau))])
            ax[2].set_xlabel("wavenumber / cm$^{-1}$")

    if len(subdata) == 1:
        subdata = subdata[0]

    return subdata
