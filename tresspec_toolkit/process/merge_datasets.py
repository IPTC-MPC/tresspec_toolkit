import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Todo: this is far from being finished. Right now we don't have a dummy dataset at hand. Finish it, when this is the
# case

def merge_datasets(dataset1, dataset2, index_ref=1, frequency_shift=0.0, delta_nu=0.3, visualize=False):
    print(dataset1)
    #  merge_datasets(data1, data2, index_ref, varargin)
    # merge_datasets is invoked to merge two measurements recorded at different center wavelengths of the polychromator
    # into one set of data
    #
    # Type merge_datasets(data1, data2, index_ref, varargin) to merge datasets
    #
    # Usage:
    # [merged] = merge_datasets(data1, data2, index_ref, varargin)
    #   - "data1":      a DataFrame containing first set of data
    #   - "data2":      a DataFrame containing second set of data
    #   - "index_ref":  a pointer to indicate which data set is considered to be the reference to which the other
    #                   one is adjusted in case of inconsistencies regarding intensities etc.
    # % optional

    if index_ref == 1:
        dataset2.index = dataset2.index + frequency_shift
    else:
        dataset1.index = dataset1.index + frequency_shift

    ################################
    #    running sanity checks:    #
    ################################
    if max(dataset1.index) < max(dataset2.index):
        spectrum_r = dataset1  # low-frequency dataset  (red)
        spectrum_b = dataset2  # high-frequency dataset (blue)
    else:
        spectrum_r = dataset2
        spectrum_b = dataset1

    # determine minimal and maxiumum values
    nu_max_r = max(spectrum_r.index)
    nu_min_b = min(spectrum_b.index)

    if nu_max_r < nu_min_b:
        print('Datasets do not cover common spectral range. Abort...')
        exit

    if len(spectrum_r.columns) != len(spectrum_b.columns):
        print("Number of delays inconsistent between measurements.")

    # input:
    # % if you want to dismiss one or more measurements, do so by optional
    # % keyword
    # "exclude"
    # followed
    # by
    # the
    # indeces
    # of
    # the
    # erroneous
    # % measurements
    # % % initialization
    # PLOT = false;
    # nu_shift = 0;
    # delta_nu = 0.3; % threshold
    # for averaging points together

    ####################################################################
    #    definition of functions used for manipulation of data sets    #
    ####################################################################
    const0 = 0.5
    const0 = [0.98, 0.5]

    def shift(dod, const):
        return dod + const

    const0 = [0.98, 0.5]

    def scale_and_shift(dod, f_sc, const):
        return f_sc * dod + const

    if index_ref == 1:
        ref = dataset1
        scalable = dataset2
    # % reference = subdata1;
    # % toscale = subdata2;
    else:
        ref = dataset2
        scalable = dataset1
    # % reference = subdata2;
    # % toscale = subdata1;

    scalable_scaled = scalable

    ref_trim = ref.ilox[(ref.index >= nu_max_r) & (ref.index <= nu_min_b), :]
    scalable_trim = scalable.iloc[(scalable.index >= nu_max_r) & (scalable.index <= nu_min_b), :]

    for delay in spectrum_r.columns:
        # CONST = curve_fit(signal_with_constant_offset, const0,
        # spline(scalable_trim.index, scalable_trim.loc[:, delay], ref_trim.index), ref_trim.loc[:, delay]

        #    scalable_scaled(2: end, n + 1) = signal_with_constant_offset(CONST(n,:), scalable(2: end, n + 1));

        if visualize:
            fig, ax = plt.subplots()
            ax.plot(ref_trim.index, ref_trim.loc[:, delay], marker='bo-')
            ax.plot(ref.index, ref.loc[:, delay], marker='b:')
            ax.plot(scalable_trim.index, scalable_trim.loc[:, delay], marker='ro-')
            ax.plot(scalable.index, scalable.loc[:, delay], marker='r:')
            # ax.plot(scalable.index, signal_with_constant_offset(CONST(n,:), scalable(2: end, n + 1)), 'g-')

            ax.legend('common data (1)', 'first data set', 'common data (2)', 'second data set',
                      'adjusted and stitched')

#######################################################################################################################
# still under construction!!!!

#
#
#
# merged = [ref;
# scalable_scaled(2: end,:)];
#
# merged(2: end,:) = sortrows(merged(2: end,:), 1);
#
# merged = CLP_average(merged, delta_nu);
#
# if PLOT
#     figure
#     plot(merged(2: end, 1), merged(2: end, 2: end))
#     end
#
# end
#
# % % average
# spectrally
# close
# lying
# points
# together
# function[corrdata] = CLP_average(data, threshold)
#
# corrdata = data(1,:);
#
# for i = 2:size(data, 1)
# A = data(abs(data(:, 1) - data(i, 1)) < threshold,:);
# tmp(i - 1,:) = mean(A, 1);
# end
#
# tmp = unique(tmp, 'rows');
# tmp = sortrows(tmp, 1);
# corrdata = [corrdata;
# tmp];
# % corrdata
#
# end
#
# % % average
# spectrally
# close
# lying
# points
# together
# function[corrdata] = clp_average(data, threshold)
#
# tempdata = data;
#
# for i = 2:size(tempdata, 1)
#
# % tempdata(i, 1)
# dummymatrix = data;
# dummymatrix(i,:) = []; % removing
# line
#
# % A = abs(dummymatrix(:, 1) - tempdata(i, 1));
# % minA = min(A);
# % TEMP = data(abs(dummymatrix(:, 1)-tempdata(i, 1)) == minA,:);
# % closest = TEMP(1,:);
#
#
# closest = FCLentry(dummymatrix, 1, tempdata(i, 1));
#
# if (abs(closest(1, 1) - tempdata(i, 1))) < threshold
#     tempdata(i,:) = mean([closest;
#     tempdata(i,:)], 1); % avarage
#     each
#     row
#     together
# end
# end
#
# tempdata = unique(tempdata, 'rows');
#
# corrdata = tempdata;
# end
#
# % %
# function
# f = FCLentry(data, col, nu)
# % % % fclosestentry
# returns
# row
# of
# an
# array
# for which the value in data(:,
# col)
# % % % is closest
# to
# nu
# % % % Type
# fclosestentry(data, col, nu)
# to
# find
# the
# row in dataset
# "data"
# % % % for which the entry in the column specified by "col" (data(:,
# col)) is
# % % % as close as possible
# to
# the
# value
# specified
# by
# "nu".
# % %
# A = abs(data(:, col) - nu);
# minA = min(A);
# tempdata = data(abs(data(:, col) - nu) == minA,:);
# % if multiple matches make sure to use first
# f = tempdata(1,:);
# % data(abs(data(:, col) - nu) == minA,:);
# end
# % %
# %
