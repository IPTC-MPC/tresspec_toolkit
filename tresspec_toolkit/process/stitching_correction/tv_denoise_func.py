import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar


def tv_denoise(noisy_data, wns, sb, noise):

    # unpack
    st_noise = np.array(noise[:sb])
    p2p_noise = np.array(noise[sb:])

    # create vectors by replicating values
    noise = np.tile(st_noise, int(len(noisy_data)/sb))
    p2p_noise = np.tile(np.concatenate((p2p_noise, -p2p_noise)), int(len(noisy_data)/(2*sb)))

    # subtract from noisy data and calculate total_variation (which is to be minimized)
    noisy_data = noisy_data - noise - p2p_noise
    tv = sum(abs(np.diff(noisy_data)/np.diff(wns)))

    return tv


def tv_denoise2(noisy_data, wns, noise1, noise2):

    noise = np.tile(np.array([noise1, noise2]), int(len(noisy_data)/2))

    # subtract from noisy data and calculate tv (which is to be minimized)
    noisy_data = noisy_data - noise
    tv = sum(abs(np.diff(noisy_data)/np.diff(wns)))

    return tv


def tv_denoise_with_scaling(noisy_data, delay, noise):
    # unpack
    sb = len(noisy_data)
    f_sc_noise_paras = np.array(noise[:sb])
    st_noise_paras = np.array(noise[sb:2 * sb])
    p2p_noise_paras = np.array(noise[2 * sb:])

    # create empty list
    manipulated_data = list()
    for idx, st_run in enumerate(noisy_data):
        manipulated_data.append(f_sc_noise_paras[idx] * noisy_data[idx].loc[delay, :]
                                - st_noise_paras[idx]
                                - p2p_noise_paras[idx] * np.cos(np.pi * np.arange(0, len(noisy_data[idx].columns), 1)))

    # merge and sort in ascending order wrt. wavelengths
    manipulated_data_merged = pd.concat(manipulated_data).sort_index()

    ############################################################
    # for troubleshooting, plot results
    # fig, (ax1, ax2, ax3) = plt.subplots(3)
    # for idx, st_run in enumerate(noisy_data):
    #     ax1.plot(st_run.columns, st_run.loc[delay, :] + idx * 0.5, label="stitching run " + str(idx), marker="o")
    #     ax2.plot(manipulated_data[idx].index, manipulated_data[idx] + idx * 0.5,
    #     label="stitching run " + str(idx), marker="o")
    #
    # ax1.legend()
    # ax2.legend()
    # ax3.plot(manipulated_data_merged.index, manipulated_data_merged, marker="o")
    #
    # plt.xlabel("wavelength / nm")
    #
    ############################################################


    # subtract from noisy data and calculate total_variation (which is to be minimized)
    tv = sum(abs(np.diff(manipulated_data_merged)/np.diff(manipulated_data_merged.index)))

    return tv
