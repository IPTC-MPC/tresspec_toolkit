import numpy as np
import pandas as pd
from scipy import stats


def create_pointer(axis, ranges=None, closest_to=None):
    """
    A function to create pointer arrays that are used to slice a DataFrame extracting the data of interest

    :param axis:        the vector to apply this function to (e.g. the frequency or the delay axis)
    :param ranges:      the ranges of interest provided as [[..., ...], [..., ....], ...]
    :param closest_to:  specify discrete value(s) to find the closest match in the data matrix
    :return:
    """

    ##########################################################
    # setting defaults
    pointer = np.array([])

    if ranges is None:
        ranges = [[-np.inf, np.inf]]

    ##########################################################

    if closest_to is not None:
        if not isinstance(closest_to, list):
            closest_to = [closest_to]

        for value in closest_to:
            pointer = np.append(pointer, (np.abs(axis - value)).argmin())
    else:
        for subrange in ranges:
            indices = np.where(np.logical_and(axis >= min(subrange), axis <= max(subrange)))[0]
            pointer = np.append(pointer, indices)

    pointer = np.sort(pointer)

    return pointer


def trim_dataset_rev(datasets, spectral_ranges=None, time_ranges=None, delays_explicit=None,
                     spectral_positions_explicit=None):

    """
    Invoke to trim dataset(s) to a specific temporal and spectral range
    :param datasets:                        a pandas DataFrame storing the data (or a list thereof)
    :param time_ranges:                     the time range(s) of interest (format: [[..., ...], ....]
    :param spectral_ranges:                 the spectral range(s) of interest (format: [[..., ...], ....]
    :param delays_explicit:                 an explicit list of delays of interest
    :param spectral_positions_explicit:     an explicit list of spectral positions of interest
    :return:                                a pandas DataFrame storing the data trimmed to the desired temporal and
                                            spectral range (or a list thereof)
    """

    ####################################################################################################################
    # setting defaults
    if not isinstance(datasets, list):
        datasets = [datasets]

    if time_ranges is None:
        time_ranges = [[-np.inf, np.inf]]
    if spectral_ranges is None:
        spectral_ranges = [[-np.inf, np.inf]]

    if isinstance(spectral_positions_explicit, np.ndarray):
        spectral_positions_explicit = spectral_positions_explicit.tolist()

    trimmed_datasets = list()

    ####################################################################################################################
    for dataset in datasets:

        row_pointer = create_pointer(dataset.index, ranges=spectral_ranges, closest_to=spectral_positions_explicit)
        col_pointer = create_pointer(dataset.columns, ranges=time_ranges, closest_to=delays_explicit)

        trimmed_datasets.append(dataset.iloc[row_pointer, col_pointer])

    ####################################################################################################################
    if len(trimmed_datasets) == 1:
        trimmed_datasets = trimmed_datasets[0]

    return trimmed_datasets
