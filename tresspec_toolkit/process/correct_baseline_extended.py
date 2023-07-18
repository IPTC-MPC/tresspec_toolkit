import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def correct_baseline_extended(datasets, time_ranges, degrees, spectral_ranges):

    """
    correct_baseline subjects a dataset to a baseline  correction by fitting polynomials to the baseline and
    subtracting them from the baseline - shifted data set
    #
    # A polynomial fit of degree "degree(i)" is performed to the baseline in the range specified from "nu(2*i-1)" to
    # "nu(2*i)".Between these ranges a linear interpolation is applied to prevent affection of the real signals.

    :param datasets:            a list containing the separate measurements as pandas DataFrames
    :param time_ranges:         a list of lists containing the ranges along the delay axis for which operations are to
                                be applied
    :param degrees:             the degree of the polynomial used for fitting the baseline
    :param spectral_ranges:     a list containing of lists containing the spectral ranges used to calculate the baseline

    :param plot:                whether to make plots
    :param apply_before_zero:   boolean whether to apply baseline correction also for negative delays.
                                Defaults to "False"
    :return:                    the baseline corrected dataset
    """

    datasets_baseline_corrected = list()
    baselines = list()

    if not isinstance(datasets, list):
        datasets = [datasets]

    # entering loop to apply baseline correction
    for counter, data in enumerate(datasets):
        print(f"")
        print(f"Baseline correction of dataset {counter+1} ({counter+1}/{len(datasets)})")

        baseline_mat = pd.DataFrame(np.zeros_like(data), index=data.index, columns=data.columns)

        for (time_range, degree, spectral_range) in zip(time_ranges, degrees, spectral_ranges):

            # create array of bounds
            bounds = np.array(spectral_range, dtype=float)
            bounds = np.insert(bounds, 0, -np.inf)
            bounds = np.append(bounds, np.inf)
            bounds = np.sort(bounds)

            lower_bounds = bounds[0::2]
            upper_bounds = bounds[1::2]

            tmp_data = data.iloc[:, (data.columns >= min(time_range)) & (data.columns <= max(time_range))]

            for (lower_bound, upper_bound) in zip(lower_bounds, upper_bounds):
                #print(f"Dropping rows with row indices between {lower_bound} and {upper_bound}")
                tmp_data = tmp_data.drop(
                    index=tmp_data[(tmp_data.index > lower_bound) & (tmp_data.index < upper_bound)].index)

            print(f"Performing baseline correction for spectra at delays between {time_range[0]} and {time_range[1]}")
            print(f" ... calculating baseline from range(s) {spectral_range}")
            print(f" ... modeling baseline by polynomial of degree {degree}")
            print(f"")

            pp = np.polynomial.polynomial.polyfit(tmp_data.index, tmp_data, degree)

            #baseline = np.polynomial.polynomial.polyval(tmp_data.index.values, pp)


            baseline_mat.iloc[:,
            (baseline_mat.columns >= min(time_range)) & (baseline_mat.columns <= max(time_range))] = \
                np.polynomial.polynomial.polyval(baseline_mat.index.values, pp).transpose()

        cleared_data = data - baseline_mat

        datasets_baseline_corrected.append(data - baseline_mat)
        baselines.append(baseline_mat)

    return datasets_baseline_corrected, baselines
