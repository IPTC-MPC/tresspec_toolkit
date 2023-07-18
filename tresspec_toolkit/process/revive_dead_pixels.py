import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp2d


def revive_dead_pixels(runs_sb, dead_pixels=None, spline_mode="cubic", plot=False):

    """

    :param runs_sb:
    :param dead_pixels:
    :param spline_mode:
    :param plot:
    :return:
    """

    runs_revived = list()
    runs_revived_sb = list()

    for run in runs_sb:
        sb_revived = list()
        for sb in run:
            nu_corrupted = sb.columns
            tau_corrupted = sb.index

            if isinstance(dead_pixels, list):
                dead_pixels_internal = [i - 1 for i in dead_pixels]
            elif isinstance(dead_pixels, np.ndarray):
                dead_pixels_internal -= 1

            # remove corrupted pixels to get a clean model how the signal is supposed to look
            data_dead_pixels_removed = sb.drop(columns=sb.columns[dead_pixels_internal])

            # create a grid interpolation function using uncorrupted data points
            tau_good = data_dead_pixels_removed.index.values
            nu_good = data_dead_pixels_removed.columns.values
            dod = data_dead_pixels_removed.values

            # create a grid interpolation function using uncorrupted data points
            f = interp2d(nu_good, tau_good, dod, kind=spline_mode)

            # use this function to re-interpolate to the initial grid and parse into DataFrame
            # please not that fliplr is necessary because of internal sorting of nu_corrupted during interpolation
            data_dead_pixels_revived = pd.DataFrame(np.fliplr(f(nu_corrupted, tau_corrupted)),
                                                    index=tau_corrupted, columns=nu_corrupted)

            # add to list of results
            sb_revived.append(data_dead_pixels_revived)

            # if plot flag is set create images to illustrate performance
            if plot:
                fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
                ax1.set_title("raw data (with zombies)")
                ax1.imshow(sb)
                ax2.set_title("dead pixels revived")
                ax2.imshow(data_dead_pixels_revived)
                ax3.set_title("residuals (raw data - cleared data")
                ax3.imshow(sb - data_dead_pixels_revived)

                # plots
                fig, axs = plt.subplots(3, 1, sharex=True)
                axs[0].plot(sb.T, marker="o")
                axs[0].set_ylabel("$\Delta$mOD")

                axs[1].plot(data_dead_pixels_revived.T)
                axs[1].set_ylabel("$\Delta$mOD")

                axs[2].plot(sb.T - data_dead_pixels_revived.T)
                axs[2].set_ylabel("$\Delta$mOD")
                axs[2].set_xlabel("wavelength / nm")

        runs_revived_sb.append(sb_revived)

        # transform back
        runs_revived.append(pd.concat(runs_revived_sb[-1], axis=1).transpose())

        runs_revived[-1].index = 10**7 / runs_revived[-1].index
        runs_revived[-1] = runs_revived[-1].sort_index(axis=0)

    return runs_revived, runs_revived_sb
