from tresspec_toolkit.process.stitching_correction.methods.tv_denoise import *
import pandas as pd
import numpy as np
import copy

from .visualize.visualize import visualize
from .misc.print_progress_bar import print_progress_bar
from .misc.DataStitchingNoiseReduced import DataStitchingNoiseReduced
from .misc.write_sve_dat_file import write_sve_dat_file


def denoise(runs_sb, method="tv_denoise", plot=False, pause_plot=1, save_corrected_data=True):
    """

    :param runs_sb:             compilation of measurements separated into their respective stitching runs
    :param method:              method to apply for correction of systematic noise due to stitching procedure
                                (defaults to "tv_denoise")
    :param plot:                boolean whether to plot the results of the denoising algorithm for graphical assertion
                                of the performance of the method
    :param pause_plot:          the duration in second to show the results for each delay (used in combination with
                                "plot=" flag to interface with "visualize" function)
    :param save_corrected_data: boolean whether to write the corrected data to drive
    :return:                    an instance of the DataStitchingNoiseReduced class containing all the
                                required information
    """


    def update_results(old_data, index_of_run, tau, update_by):
        updated_data = old_data

        for idx_st_run, new_data in enumerate(update_by):
            updated_data[index_of_run][idx_st_run].loc[tau, :] = new_data

        return updated_data

    # extracting number of measurements, stitching runs and delays
    no_runs = len(runs_sb)
    no_st_runs = len(runs_sb[0])
    no_delays = len(runs_sb[0][0].index)

    print("Reducing systematic noise due to stitching procedure by applying ", method, " algorithm...")

    # preparing variables to store results of denoising algorithm
    st_noise_df = copy.deepcopy(runs_sb)
    p2p_noise_df = copy.deepcopy(runs_sb)
    runs_sb_cleared = copy.deepcopy(runs_sb)

    i = 1

    ##################################################################
    #    loop over runs and delays to correct each one separately    #
    ##################################################################
    for idx_run, run in enumerate(runs_sb):
        delays = run[0].index
        for delay in delays:

            if method == "tv_denoise":
                denoised_data, res1, st_noise, p2p_noise = tv_denoise(run, delay)

                # update results
                st_noise_df = update_results(st_noise_df, idx_run, delay, st_noise)
                p2p_noise_df = update_results(p2p_noise_df, idx_run, delay, p2p_noise)
                runs_sb_cleared = update_results(runs_sb_cleared, idx_run, delay, denoised_data)

            # update progress bar
            print_progress_bar(i, no_runs*no_delays, (idx_run+1), no_runs, delay)
            i = i+1

    #########################################################################
    #    compile results as an object of DataStitchingNoiseReduced class    #
    #########################################################################
    results = DataStitchingNoiseReduced(method, runs_sb, st_noise_df, p2p_noise_df, runs_sb_cleared)

    ###############################################################
    #    visualize results of denoising algorithm (if desired)    #
    ###############################################################
    if plot:
        visualize(results, pause_time=pause_plot)

    ##########################################################
    #    write results to files to be reused if necessary    #
    ##########################################################
    if save_corrected_data:
        write_sve_dat_file(results.cleared_data_sb, filename="denoised_data")
        write_sve_dat_file(results.raw_data_sb, filename="raw_data")
        write_sve_dat_file(results.st_noise, filename="stitching_noise")
        write_sve_dat_file(results.p2p_noise, filename="pixel_to_pixel_noise")

    return results, runs_sb_cleared, st_noise_df, p2p_noise_df
