import numpy as np
import pandas as pd
from scipy import stats


def extract_selected_delays(datasets, delays=None):

    """
    Invoke to extract specific delays from a dataset of time-resolved spectroscopic data

    :param datasets:    a pandas DataFrame storing the data (or a list thereof)
    :param delays:      the delays of interest (either as int/float or as a list thereof);
                        the closest match is returned if the time axis does not contain a delay explicitly
    :return:            the time-resolved spectra for these specific delays
    """

    delays.sort()

    if not isinstance(datasets, list):
        datasets = [datasets]

    subdata = list()
    for dataset in datasets:
        tmp = list()
        for delay in delays:
            tmp0 = dataset.iloc[:, abs(dataset.columns - delay) == min(abs(dataset.columns - delay))]
            tmp.append(tmp0)

        subdata.append(pd.concat(tmp, axis=1))

    if len(subdata) == 1:
        subdata = subdata[0]

    return subdata
