import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def dod_denoise(dod_noisy, delay, resx, visualize=False):

    sb = len(dod_noisy)

    dod_denoised = list()
    dod_noisy_merged = list()
    for idx, st_run in enumerate(dod_noisy):
        # compile noisy data into one
        dod_noisy_merged.append(st_run.loc[delay, :])

        # alter the dataset by the previously determined parameters
        if len(resx) == 3 * sb:
            dod_denoised.append(resx[idx] * st_run.loc[delay, :]
                                - resx[sb + idx]
                                - resx[2 * sb + idx] * np.cos(np.pi * np.arange(0, len(st_run.columns), 1)))
        elif len(resx) == 2 * sb:
            dod_denoised.append(st_run.loc[delay, :]
                                - resx[idx]
                                - resx[sb + idx] * np.cos(np.pi * np.arange(0, len(st_run.columns), 1)))

    # make pandas series out of individual datasets
    dod_noisy_merged = pd.concat(dod_noisy_merged).sort_index()
    dod_denoised_merged = pd.concat(dod_denoised).sort_index()

    #############################################################################
    # if requested:
    # visualize result of denoising function for visual inspection and evaluation
    if visualize:
        # visualization
        fig, (ax1, ax2, ax3) = plt.subplots(3)

        # plot of separate stitching runs
        for idx, st_run in enumerate(dod_noisy):
            # label = ("stitching run " + str(idx+1) + " (f_sc = " + str(resx[idx]) + ", sb_offset = "
            #          + str(resx[sb + idx]) + ", p2p = " + str(resx[2 * sb + idx]) + ")")
            ax1.plot(st_run.columns, st_run.loc[delay, :],
                     label="stitching run" + str(idx + 1) + " (raw data)", marker="o")

            ax2.plot(dod_denoised[idx].index, dod_denoised[idx],
                     label="stitching run" + str(idx + 1) + " (f_sc = " + str(resx[idx]),
                     marker="o")

        ax1.set_ylabel("$\mathregular{\Delta}$mOD")
        ax2.set_ylabel("$\mathregular{\Delta}$mOD")
        ax3.set_ylabel("$\mathregular{\Delta}$mOD")
        ax1.legend()
        ax2.legend()

        # plot of merged data before and after denoising
        ax3.plot(dod_noisy_merged.index, dod_noisy_merged, label="raw data", marker="o")
        ax3.plot(dod_denoised_merged.index, dod_denoised_merged, label="denoised data", marker="o")
        ax3.legend()

        #############################################################################

        # offset = 1.0
        #
        # ax2.plot(dod_noisy_merged.columns, dod_noisy_merged, label="noisy raw data", marker="o")
        # ax2.plot(dod_denoised_merged.columns, dod_denoised_merged + offset, label="denoised data (+ 1.0)", marker="o")
        # ax2.set_ylabel("$\mathregular{\Delta}$mOD")
        # ax2.legend()
        #
        # ax3.plot(dod_noisy_merged.columns, dod_noisy_merged - dod_denoised_merged,
        #          label="residuals raw data - smoothed data")
        # ax3.set_ylabel("$\mathregular{\Delta}$ $\mathregular{\Delta}$mOD")
        # ax3.legend()

        plt.xlabel("wavenlength / nm")

    return dod_denoised
