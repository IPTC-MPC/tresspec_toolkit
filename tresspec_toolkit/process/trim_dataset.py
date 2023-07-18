import numpy as np
import pandas as pd
from scipy import stats


def trim_dataset(datasets, spectral_range=[-np.inf, np.inf], time_range=[-np.inf, np.inf], delays_explicit=None,
                 spectral_positions_explicit=None):

    """
    Invoke to trim dataset(s) to a specific temporal and spectral range
    :param datasets:                        a pandas DataFrame storing the data (or a list thereof)
    :param time_range:                      the time range of interest
    :param spectral_range:                  the spectral range of interest
    :param delays_explicit:                 an explicit list of delays of interest
    :param spectral_positions_explicit:     an explicit list of spectral positions of interest
    :return:                                a pandas DataFrame storing the data trimmed to the desired temporal and
                                            spectral range
    """

    print("This function is outdated. Use the improved version 'trim_dataset_rev' instead which offers more flexibility")

    time_range.sort()
    spectral_range.sort()

    def find_nearest(arr, values):
        indices = list()
        arr = np.asarray(arr)
        for value in values:
            indices.append((np.abs(arr - value)).argmin())
        return indices

    if not isinstance(datasets, list):
        datasets = [datasets]

    subdata = list()
    for dataset in datasets:

        if delays_explicit is not None and spectral_positions_explicit is not None:
            sub = dataset.iloc[find_nearest(dataset.index, spectral_positions_explicit),
                               find_nearest(dataset.columns, delays_explicit)]
        elif delays_explicit is not None and spectral_positions_explicit is None:
            sub = dataset.iloc[(dataset.index >= min(spectral_range)) & (dataset.index <= max(spectral_range)),
                               find_nearest(dataset.columns, delays_explicit)]
        elif delays_explicit is None and spectral_positions_explicit is not None:
            sub = dataset.iloc[find_nearest(dataset.index, spectral_positions_explicit),
                               (dataset.columns >= min(time_range)) & (dataset.columns <= max(time_range))]
        else:
            sub = dataset.iloc[(dataset.index >= min(spectral_range)) & (dataset.index <= max(spectral_range)),
                               (dataset.columns >= min(time_range)) & (dataset.columns <= max(time_range))]

        subdata.append(sub)

    if len(subdata) == 1:
        subdata = subdata[0]

    return subdata
