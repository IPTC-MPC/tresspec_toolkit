import numpy as np
import pandas as pd


def tv_denoise(noisy_data, delay, noise):
    # unpack
    sb = len(noisy_data)
    st_noise_paras = np.array(noise[:sb])
    p2p_noise_paras = np.array(noise[sb:])

    # create empty list
    manipulated_data = list()
    for idx, st_run in enumerate(noisy_data):
        manipulated_data.append(noisy_data[idx].loc[delay, :]
                                - st_noise_paras[idx]
                                - p2p_noise_paras[idx] * np.cos(np.pi * np.arange(0, len(noisy_data[idx].columns), 1)))

    # merge and sort in ascending order wrt. wavelengths
    manipulated_data_merged = pd.concat(manipulated_data).sort_index()

    # subtract from noisy data and calculate total_variation (which is to be minimized)
    tv = sum(abs(np.diff(manipulated_data_merged)/np.diff(manipulated_data_merged.index)))

    return tv
