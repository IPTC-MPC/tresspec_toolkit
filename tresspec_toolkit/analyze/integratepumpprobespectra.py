import numpy as np
import scipy
import pandas as pd
import matplotlib.pyplot as plt


def integratepumpprobespectra(data, time_range=[0, np.inf], spectral_range=[-np.inf, np.inf], plot=False,
                              semilog=False):

    """
    :param data:            the dataset to be subjected to this analysis (provided as a pandas DataFrame)
    :param time_range:      a list containing the lower and upper limits of the time range used to perform this analysis
    :param spectral_range:  a list containing the lower and upper limits of the spectral range used to perform this
                            analysis
    :param plot:            boolean whether to create a plot of the absorption-to-bleach ratio as a function of time
    :param semilog:         boolean whether to plot the scatter plot in a semilogarithmic fashion with respect to the
                            time domain
    :return:
    """

    # sort in ascending order
    spectral_range.sort()
    time_range.sort()

    # trimming dataset:
    tmp = data.iloc[(data.index >= spectral_range[0]) & (data.index <= spectral_range[1]),
                    (data.columns >= time_range[0]) & (data.columns <= time_range[1])]

    # make sure data are ordered in ascending order
    tmp = tmp.sort_index()

    # calculating approximate integrals by cumulative trapezoid integral
    cumtrapz = scipy.integrate.cumtrapz(tmp, tmp.index, axis=0, initial=0)

    difference = np.diff(cumtrapz, axis=0)

    a_bleach = np.sum(difference, axis=0, where=difference < 0)
    a_absorption = np.sum(difference, axis=0, where=difference >= 0)

    # calculate ratio of integrals
    # if not applicable due to integral of bleach being zero set nan instead
    a_ratio = abs(a_absorption / np.where(a_bleach != 0, a_bleach, np.nan))

    result = pd.DataFrame(np.vstack((a_absorption, a_bleach, a_ratio)),
                          index=['Absorption', 'Bleach', 'Ratio Abs./Bl.'], columns=tmp.columns)

    if plot:
        fig, ax = plt.subplots()
        ax.scatter(result.columns, result.loc["Ratio Abs./Bl.", :], color="b")
        ax.set_xlabel("t / ps")
        ax.set_ylabel("$\mathregular{A_{abs}}$ / $\mathregular{A_{bleach}}$")

        if semilog:
            ax.set_xscale("log")

    return result
