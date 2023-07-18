from tresspec_toolkit.analyze.fitfunctions import *
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import pandas as pd

from tresspec_toolkit.plotting.config.figure_descriptors import Measurement


class FitResults:
    def __init__(self, fit_function, x, y, popt, pconv, fitted_curve):
        self.fit_function = fit_function
        self.x = x
        self.y = y
        self.popt = popt
        self.pconv = pconv
        self.fitted_curve = fitted_curve


def fitting(inp, ydata=None, fitfunctions=None, plot=False, type_of_measurement=None, initial_guess=None,
             time_range=[0.1, np.inf]):

    """

    :param inp:
    :param ydata:
    :param fitfunctions:        a list of the functions used to fit the traces
    :param plot:                boolean whether to plot the fits or not
    :param type_of_measurement: the type of the measurement the data stem from
    :param initial_guess:       list of initial guesses of fitting parameters
    :param time_range:          the time range which shall be plotted
    :return:                    an instance of the FitResults class that stores all relevant information
    """

    # get the flags for creating a plot is that is desired
    measurement_flags = Measurement(type_of_measurement)

    # checking whether the input is provided as a pandas DataFrame, if not create one
    if isinstance(inp, pd.core.frame.DataFrame):
        df = inp
    else:
        try:
            df = pd.DataFrame(ydata, index=inp)
        except ValueError:
            df = pd.DataFrame(ydata.transpose(), index=inp)

    # check that the fit functions are provided as a list, if not create one
    if not isinstance(fitfunctions, list):
        print("fitfunctions is no list")
        fitfunctions = [fitfunctions]


    results = {}
    rresults = {}
    test_results = list()
    for idx, trace in enumerate(df.index):

        key = str(int(round(trace, 0)))

        #print(key)
        tau = df.columns[(df.columns >= min(time_range)) & (df.columns <= max(time_range))].to_numpy()
        #print(tau)
        dod = df.iloc[idx, (df.columns >= min(time_range)) & (df.columns <= max(time_range))]
        #print("trimmed")
        #print(dod)
        dod = dod.to_numpy()
        ###

        if initial_guess is not None:
            print(f"Using initial guess to fit trace at {trace} ...")
            popt, pconv = curve_fit(fitfunctions[idx], tau, dod, p0=initial_guess[idx])
        else:
            popt, pconv = curve_fit(fitfunctions[idx], tau, dod)

        #test_result = FitResults(fitfunction,
        #                          popt, pconv,
        #                          df.index, fitfunction(df.index, *popt), )

        #test_results.append(test_result)

        results[key] = (popt, pconv)

        rresults[key] = FitResults(fitfunctions[idx],
                                          tau, dod,
                                          popt, pconv,
                                          fitfunctions[idx](tau, *popt))


    #popt, pconv = curve_fit(fitfunction, inp, inp2)

    if plot:
        fig, ax = plt.subplots()
        for idx, trace in enumerate(df.columns):
            ax.scatter(df.index, df.loc[:, trace], label=str(trace) + " " + measurement_flags.timescale)

            # fitting
            #popt, pconv = curve_fit(fitfunction, df.index, df.loc[:, trace])
            ax.plot(df.index, fitfunctions[idx](df.index, *results[str(trace)][0]), label="fit " + str(trace))
        ax.set_xlabel(measurement_flags.ylabel)
        ax.set_ylabel(measurement_flags.zlabel)
        ax.legend()

    return rresults

