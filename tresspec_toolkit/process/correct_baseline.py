import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def correct_baseline(datasets, spectral_ranges=[-np.inf, np.inf], degree=0, plot=False, apply_before_zero=False):

    """
    correct_baseline subjects a dataset to a baseline  correction by fitting polynomials to the baseline and
    subtracting them from the baseline - shifted data set
    #
    # A polynomial fit of degree "degree(i)" is performed to the baseline in the range specified from "nu(2*i-1)" to
    # "nu(2*i)".Between these ranges a linear interpolation is applied to prevent affection of the real signals.

    :param datasets:            a list containing the separate measurements
    :param spectral_ranges:     a list containing the lower and upper bound of the range to use for fitting a baseline
    :param degree:              the degree of the polynomial used for fitting the baseline
    :param plot:                whether to make plots
    :param apply_before_zero:   boolean whether to apply baseline correction also for negative delays.
                                Defaults to "False"
    :return:                    the baseline corrected dataset
    """


    print("This function is outdated. Use the improved version 'correct_baseline_rev' instead which offers more flexibility")

    if type(datasets) != list:
        datasets = [datasets]

    bl_corrected_datasets = list()

    ##########################################
    #    loop through individual datasets    #
    ##########################################
    for dataset in datasets:
        # extract data used for calculation of baseline
        baseline_range = dataset.iloc[(dataset.index >= min(spectral_ranges))
                                      & (dataset.index <= max(spectral_ranges)), :]

        # initialize array to store baselines
        baseline = np.zeros(dataset.shape)

        # loop over delays and fit baseline to each one separately
        for idx, delay in enumerate(dataset.columns):

            if delay < 0 and not apply_before_zero:
                continue
            else:
                # perform polynomial fit to baseline
                p = np.polynomial.polynomial.polyfit(baseline_range.index, baseline_range.loc[:, delay], degree)

                # evaluate baseline data
                baseline[:, idx] = np.polynomial.polynomial.polyval(dataset.index, p)

        # subtract baseline from dataset
        bl_corrected_dataset = dataset - baseline

        # dump corrected dataset back into list
        bl_corrected_datasets.append(bl_corrected_dataset)

        if plot:
            for idx, delay in enumerate(dataset.columns):
                fig, ax = plt.subplots()
                ax.plot(dataset.index, dataset.loc[:, delay],
                        label="raw data")
                ax.plot(baseline_range.index, baseline_range.loc[:, delay], marker="o", linestyle="None",
                        label="data used to fit baseline")
                ax.plot(dataset.index, baseline[:, idx],
                        label="baseline")
                ax.plot(bl_corrected_dataset.index, bl_corrected_dataset.loc[:, delay],
                        label="data after baseline subtraction")

            ax.legend()

    if len(bl_corrected_datasets) == 1:
        bl_corrected_datasets = bl_corrected_datasets[0]

    return bl_corrected_datasets




# % %
# regions = size(nu, 1);
# delays = size(data, 2) - 1;
#
# index = zeros(size(nu));
#
# baselinecorrecteddata = data;
#
    # preparing a matrix to store the fitted baselines
# baseline = zeros(size(data));
# baseline(2: end, 1)      = data(2: end, 1);
# baseline(1, 2: end)      = data(1, 2: end);
#
# data_for_baseline = [];
#
# % this is the
# normal
# case
# that
# we
# employ
# a
# single
# type
# of
# baseline
# correction
# if max(size(degree)) == 1
#     for i = 1:regions
#     data_for_baseline = [data_for_baseline;
#     ...
#     fspecregion(data, col, nu(2 * i - 1), nu(2 * i))];
#     end
#
#     for i = 1:delays
#     pp = polyfit(data_for_baseline(:, 1), ...
#     data_for_baseline(:, i + 1), degree);
#     baseline(2: end, i + 1)      = polyval(pp, data(2: end, 1));
#     end
#
#     baselinecorrecteddata(2: end, 2: end)      = data(2: end, 2: end) - baseline(2: end, 2: end);
#     % in case
#     that
#     we
#     need
#     to
#     subtract
#     different
#     polynomials
#     at
#     different
#     % ranges
#     else
#     for i = 1:regions
#     data_for_baseline = fspecregion(data, col, nu(2 * i - 1), nu(2 * i));
#
#     % find
#     index
#     of
#     first and last
#     entry
#     of
#     this
#     range
#     index(2 * i - 1) = find(data(:, 1) == data_for_baseline(1, 1));
#     index(2 * i) = find(data(:, 1) == data_for_baseline(end, 1));
#
#     for j = 1:delays
#     pp = polyfit(data_for_baseline(:, 1), ...
#     data_for_baseline(:, j + 1), degree(i));
#     baseline(index(2 * i - 1): index(2 * i), j + 1) = polyval(pp, ...
#     data_for_baseline(:, 1));
#
#     if i > 1
#         A = [baseline(index(2 * i - 2), [1 j + 1]);
#         baseline(index(2 * i - 1), [1 j + 1])];
#
#         pp2 = polyfit(A(:, 1), A(:, 2), 1);
#
#         signal = baseline(index(2 * i - 2) + 1:index(2 * i - 1) - 1, 1);
#
#         baseline(index(2 * i - 2) + 1: index(2 * i - 1) - 1, j + 1) =...
#         polyval(pp2, signal);
#     end
# end
#
# end
#
# baselinecorrecteddata(2: end, 2: end)      = data(2: end, 2: end) - baseline(2: end, 2: end);
# f = baselinecorrecteddata;
# BASELINE = baseline;
# end
# % if nargin == 5
#     % figure
#     % plot(data(2: end, 1), data(2: end, 2: end)) %, ...
#     % baselinecorrecteddata(2: end, 1), ...
#     % baselinecorrecteddata(2: end, 2: end), ...
#     % baseline(2: end, 1), baseline(2: end, 2: end))
#     % end
#       %
#       %
#       end