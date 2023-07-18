import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib
# load style specs for custom plot


def find_transients(datasets, take_traces_at=None):

    """
    Invoke to extract the transient traces at selected frequencies/wavelength
    
    :param datasets:            a pandas DataFrame storing the data (or a list thereof)
    :param take_traces_at:      a single value or a list of frequencies/wavelengths where to take transient traces at
    :return:                    a pandas DataFrame containing only the data at the desired frequencies
                                (or a list thereof)
    """

    if not isinstance(datasets, list):
        datasets = [datasets]

    if not isinstance(take_traces_at, list):
        take_traces_at = [take_traces_at]

    subdata = list()
    for dataset in datasets:
        tmp = list()
        for frequency in take_traces_at:
            tmp0 = dataset.iloc[abs(dataset.index - frequency) == min(abs(dataset.index - frequency)), :]
            tmp.append(tmp0)

        subdata.append(pd.concat(tmp, axis=0))

    if len(subdata) == 1:
        subdata = subdata[0]

    return subdata
