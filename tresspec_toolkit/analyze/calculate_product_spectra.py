import numpy as np
import pandas as pd
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt


def calculate_product_spectra(dataset, stationary_ir):

    """
    :param dataset:         the dataset(s) containing the data from the time-resolved experiment (either a pandas
                            DataFrame or list thereof)
    :param stationary_ir:   the stationary IR spectrum
    :return:
    """

    stationary_ir = stationary_ir.iloc[(stationary_ir.index >= min(dataset.index)) &
                                       (stationary_ir.index <= max(dataset.index)), :]

    ##########################################################################################
    #    calculate natural cubic spline polynomials                                          #
    #    (to project stationary spectrum onto frequency axis of time-resolved experiment)    #
    ##########################################################################################
    cs = CubicSpline(stationary_ir.index, stationary_ir.OD, bc_type='natural')

    # determine the scaling factor used to fit the intensity of the stationary spectrum to the time-resolved data
    f_sc = min(dataset.loc[:, 0]) / max(stationary_ir.OD)

    print(f"Scaling stationary IR spectrum by a factor of {f_sc} ...")


# Todo: at this stage, the fundamental concept seems to be working. However, it might lead to improvement to interpolate
# Todo: the time-resolved dataset instead. We still encounter negative going dips, probably due to insufficient sampling
# Todo: on the frequency axis

    paps = dataset.to_numpy() - f_sc * np.tile(cs(dataset.index).reshape(len(cs(dataset.index)), 1), dataset.shape[1])

    paps = pd.DataFrame(paps, index=dataset.index, columns=dataset.columns)
    return paps
