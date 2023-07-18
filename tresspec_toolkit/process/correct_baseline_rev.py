import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import interp1d
from tresspec_toolkit.process.trim_dataset_rev import *


def fill_zero_columns(df, df_trimmed):
    missing_columns = np.setdiff1d(df.columns, df_trimmed.columns)

    df_zeros = pd.DataFrame(np.zeros((len(df_trimmed.index), len(missing_columns))), index=df_trimmed.index,
                            columns=missing_columns)

    merged = pd.concat((df_trimmed, df_zeros), axis=1).sort_index(axis=1)

    return merged


def correct_baseline_rev(datasets, spectral_ranges=None, degree=None, plot=False, apply_before_zero=False,
                         piecewise=False):
    """
    correct_baseline subjects a dataset to a baseline  correction by fitting polynomials to the baseline and
    subtracting them from the baseline - shifted data set

    :param datasets:            a list containing the separate measurements
    :param spectral_ranges:     a list containing the lower and upper bounds of the ranges to use for fitting a baseline
    :param degree:              the degree of the polynomial used for fitting the baseline
    :param plot:                whether to make plots
    :param apply_before_zero:   boolean whether to apply baseline correction also for negative delays.
                                Defaults to "False"
    :return:                    the baseline corrected dataset
    """
    from scipy.linalg import lstsq
    from tresspec_toolkit.process.trim_dataset_rev import trim_dataset_rev

    ####################################################################################################################
    # setting defaults
    if not isinstance(datasets, list):
        datasets = [datasets]

    if degree is None:
        degree = 0
    if spectral_ranges is None:
        spectral_ranges = [[-np.inf, np.inf]]

    if not apply_before_zero:
        time_ranges = [[0, np.inf]]
    else:
        time_ranges = [[-np.inf, np.inf]]

    baseline_corrected_datasets = list()

    ####################################################################################################################
    for dataset in datasets:
        data_used_for_bl = trim_dataset_rev(dataset, spectral_ranges=spectral_ranges, time_ranges=time_ranges)

        # filling with zero columns (for delays that should not be subjected to baseline correction)
        data_used_for_bl = fill_zero_columns(dataset, data_used_for_bl)

        #########################################################################
        # creating the design matrix for multiple linear regression             #
        design_matrix = np.vander(data_used_for_bl.index, degree + 1)  # create a Vandermonde matrix from the nu vector

        #########################################################################
        # determine polynomial coefficients applying Multiple Linear Regression #
        beta = lstsq(design_matrix, data_used_for_bl)

        #########################################################################
        # calculate the baselines
        baseline = np.vander(dataset.index, degree+1) @ beta[0]

        baseline_corrected = dataset - baseline

        baseline_corrected_datasets.append(baseline_corrected)

        if plot:
            fig, axs = plt.subplots(3, 1, sharex=True)
            fig.subplots_adjust(wspace=0.03)
            axs[0].plot(dataset.index, dataset)
            axs[1].plot(data_used_for_bl.index, data_used_for_bl, marker="o")
            axs[1].plot(dataset.index, baseline)
            axs[2].plot(baseline_corrected.index, baseline_corrected)
            for ax in axs:
                ax.axhline(color="k", alpha=0.2)

    return baseline_corrected_datasets
