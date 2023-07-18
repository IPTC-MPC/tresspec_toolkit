import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

from scipy.optimize import minimize_scalar, minimize


def tv_denoise(dod_sb_raw, tau, plot=False):
    """
    a function to minimize the total variation of a data set by shifting the stitching runs horizontally
    :param dod_sb_raw:                  the raw transient spectrum in a sorted fashion in terms of differential optical
                                        densities
    :param tau:                         the wavelength (or frequency) axis of the transient spectrum
    :param plot:                        boolean whether to plot the results of the denoising algorithm in order to
                                        assert the performance of the function
    :return:                            denoised_data (the transient spectrum with the stitching runs being shifted in
                                        order to remove systematic stitching noise) and res1 (the results of the
                                        minimizer as returned from scipy.optimize.minimize)
    """

    number_of_stitching_blocks = len(dod_sb_raw)
    no_pixels = len(dod_sb_raw[0].columns)

    def shift_data(st_runs, delay, st_noise_paras, p2p_noise_paras):
        """
        shifts stitching runs by certain values
        :param st_runs:
        :param delay:
        :param st_noise_paras:
        :param p2p_noise_paras:
        :return:
        """
        no_pix = len(st_runs[0].columns)

        denoised_sb = list()
        for idx_st_run, st_run in enumerate(st_runs):
            denoised = st_run.loc[delay, :] - st_noise_paras[idx_st_run] - \
                       np.array([(-1) ** n for n in range(no_pix)]) * p2p_noise_paras[idx_st_run]

            denoised_sb.append(denoised)
        return denoised_sb

    def tv_functional(st_runs, delay, noise):
        """
        shifts the individual stitching runs and determines the resulting total variation
        :param st_runs: shifts the
        :param delay:
        :param noise:
        :return:
        """

        # determine number of stitching runs used for collection of the transient spectrum
        no_sb = len(st_runs)

        # shift each stitching run by its specific parameters using shift_data function
        noisy_data = shift_data(st_runs, delay, noise[:no_sb], noise[no_sb:])

        # concatenate lists to create dod and wavelength axis
        noisy_data = pd.concat(noisy_data).sort_index()
        lambda_axis = noisy_data.index

        # calculate the total variation of the manipulated data set
        tv = sum(abs(np.diff(noisy_data) / np.diff(lambda_axis)))
        return tv

    ############################################################################################
    #    minimize the functional of the total variation to determine ideal shift parameters    #
    ############################################################################################
    res1 = minimize((lambda noise: tv_functional(dod_sb_raw, tau, noise)),
                    x0=[0.1, 0.02, 0.03, -0.05, 0, 0, 0, 0])

    st_noise = list()
    p2p_noise = list()
    for idx in range(number_of_stitching_blocks):
        st_noise.append(np.ones(no_pixels) * res1.x[idx])
        p2p_noise.append(np.array([(-1) ** n for n in range(no_pixels)]) * res1.x[number_of_stitching_blocks + idx])

    ###############################################################################
    #    shift the data by the previously determined ideal shifting parameters    #
    ###############################################################################
    denoised_data = shift_data(dod_sb_raw, tau, res1.x[:number_of_stitching_blocks],
                               res1.x[number_of_stitching_blocks:])

    if plot:
        fig, ax = plt.subplots(number_of_stitching_blocks + 2, 1, sharex=True)

        for idx in range(number_of_stitching_blocks):
            ax[idx].plot(dod_sb_raw[idx].columns, dod_sb_raw[idx].loc[tau, :], marker="o",
                         label="raw data (sb = " + str(idx + 1) + ")")
            ax[idx].plot(denoised_data[idx].index, denoised_data[idx], marker="o",
                         label="denoised data")

        raw_merged = pd.concat(dod_sb_raw, axis=1).sort_index(axis=1).loc[tau, :]
        corr_merged = pd.concat(denoised_data).sort_index()
        ax[number_of_stitching_blocks].plot(raw_merged.index, raw_merged)
        ax[number_of_stitching_blocks].plot(corr_merged.index, corr_merged)

        ax[number_of_stitching_blocks + 1].plot(corr_merged.index, corr_merged - raw_merged, marker="o")

    return denoised_data, res1, st_noise, p2p_noise
