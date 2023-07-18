import numpy as np
import pandas as pd

from scipy.optimize import minimize_scalar, minimize


def tv_denoise(dod_raw, wavelength_axis, number_of_stitching_blocks):

    """
    a function to minimize the total variation of a data set by shifting the stitching runs horizontally
    :param dod_raw:                     the raw transient spectrum in a sorted fashion in terms of differential optical
                                        densities
    :param wavelength_axis:             the wavelength (or frequency) axis of the transient spectrum
    :param number_of_stitching_blocks:  the number of stitching blocks used to record the transient spectrum
    :return:                            denoised_data (the transient spectrum with the stitching runs being shifted in
                                        order to remove systematic stitching noise) and res1 (the results of the
                                        minimizer as returned from scipy.optimize.minimize)
    """

    def tv_functional(noisy_data, lambda_axis, no_sb, noise):
        no_pixels = int(len(noisy_data) / no_sb)

        st_noise = np.array(noise[:no_sb])
        p2p_noise = np.array(noise[no_sb:])

        # this is from the working version of this function; I think this might be not quite correct:

        # create vectors by replicating values
        #noise = np.tile(st_noise, no_pixels)
        #p2p_noise = np.tile(np.concatenate((p2p_noise, -p2p_noise)), int(no_pixels / 2))

        # this is a new try which I think should be more correct
        st_noise_vec = np.tile(st_noise, no_pixels)
        p2p_noise_vec = np.tile(np.concatenate((p2p_noise, -p2p_noise)), int(no_pixels/2))

        # subtract from noisy data and calculate total_variation (which is to be minimized)
        noisy_data = noisy_data - st_noise_vec - p2p_noise_vec
        tv = sum(abs(np.diff(noisy_data) / np.diff(lambda_axis)))

        return tv

    def shift_data(noisy_data, st_noise_paras, p2p_noise_paras, f_sc_paras=None):

        no_sb = len(st_noise_paras)

        no_pixels = int(len(noisy_data) / no_sb)

        if f_sc_paras is None:
            f_sc_paras = [1 for i in range(no_sb)]

        dod_denoised = np.tile(np.array(f_sc_paras), no_pixels) * noisy_data \
                       - np.tile(np.array(st_noise_paras), no_pixels) \
                       - np.tile(np.concatenate((np.array(p2p_noise_paras), -np.array(p2p_noise_paras))),
                                 int(no_pixels / 2))
        return dod_denoised

    ############################################################################################
    #    minimize the functional of the total variation to determine ideal shift parameters    #
    ############################################################################################
    res1 = minimize((lambda noise: tv_functional(dod_raw, wavelength_axis, number_of_stitching_blocks, noise)),
                    x0=[0.1, 0.02, 0.03, -0.05, 0, 0, 0, 0])

    #
    print("Optimal shifting values for stitching runs: ", res1.x[:number_of_stitching_blocks])
    print("Optimal shifting values to correct p2p noise: ", res1.x[number_of_stitching_blocks:])

    ###############################################################################
    #    shift the data by the previously determined ideal shifting parameters    #
    ###############################################################################
    denoised_data = shift_data(dod_raw, res1.x[:number_of_stitching_blocks], res1.x[number_of_stitching_blocks:])

    return denoised_data, res1
