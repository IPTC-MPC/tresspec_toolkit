import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar
import pandas as pd
from tresspec_toolkit.process import trim_dataset_rev

def vibrational_cooling(datasets, spectral_ranges=None, time_ranges=[0, np.inf],
                        degree=7, plot=False, fitfunction=None):

    """

    :param datasets:        the dataset(s) which is subjected to this analysis (either a pandas DataFrame or list
                            thereof)
    :param spectral_ranges: a list specifying the spectral range(s) which is governed by spectral shifting
    :param time_ranges:     a list specifying the time span for which the analysis should be carried out
    :param degree:          the degree of the polynomial used to fit the shape of the shifting transient absorption
                            (defaults to 7)
    :param plot:            boolean whether to create a figure of max. peak position as a function of waiting delay
    :param fitfunction:     a fitting function that is used to fit the temporal behaviour of the shifting (optional)
    :return:
    """

    if type(datasets) != list:
        datasets = [datasets]
    if len(spectral_ranges) == 2:
        print("oops, we got here, convert it")
        spectral_ranges = [spectral_ranges]


    # sanity check
    #if length(unique([size(spectral_range, 1); size(time_range, 1); length(degree)])) ~=1
    #error('Numbers of spectral window(s), temporal window(s) and/or degree(s) do not match')
    #end

    # trimming dataset if required
    vibrational_shifting = list()
    for dataset in datasets:
        nu_max = list()
        for spectral_range in spectral_ranges:


            # subdata = trim_dataset_rev(dataset, spectral_ranges=spectral_range, time_ranges=time_ranges)

            subdata = dataset.iloc[(dataset.index >= min(spectral_range)) & (dataset.index <= max(spectral_range)),
                                   (dataset.columns >= min(time_ranges)) & (dataset.columns <= max(time_ranges))]


            no_delays = subdata.shape[1]
            nu_max_tmp = np.empty(no_delays)
            for idx, delay in enumerate(subdata.columns):
                pp = np.polynomial.polynomial.polyfit(subdata.index, subdata.loc[:, delay], degree)
                polynomial_function = np.poly1d(np.flipud(pp))


               # fig, ax = plt.subplots()
               # ax.plot(subdata.index, subdata.loc[:, delay], marker="o")
               # ax.plot(subdata.index, np.polynomial.polynomial.polyval(subdata.index, pp))

                # find mimium of inverse of polynomial (effectively finding local maximum in range)
                fit = minimize_scalar(-polynomial_function, bounds=(min(subdata.index), max(subdata.index)),
                                      method='bounded')

                print(fit.x)


                nu_max_tmp[idx] = fit.x

            # append to list
            nu_max.append(pd.DataFrame(nu_max_tmp, index=subdata.columns.to_numpy(), columns=[np.mean(spectral_range)]))

        vibrational_shifting.append(pd.concat(nu_max, axis=1))

    if plot:
        for dataset in vibrational_shifting:
            for frequncy_range in dataset.columns:
                fig, ax = plt.subplots()
                ax.scatter(dataset.index, dataset.loc[:, frequncy_range], color="b")
                ax.set_xlabel("t / ps")
                ax.set_ylabel("$\\tilde{\\nu}_{max}$ / $\mathregular{cm^{-1}}$")
                ax.set_title("spectral shifting of signal")

    # unpack list if contains only one entry
    if len(vibrational_shifting) == 1:
        vibrational_shifting[0] = vibrational_shifting

    return vibrational_shifting
