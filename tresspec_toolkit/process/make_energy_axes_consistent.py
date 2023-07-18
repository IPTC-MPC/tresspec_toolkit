import pandas as pd
import numpy as np
from scipy.interpolate import interp2d


def make_energy_axis_consistent(dataset1, dataset2, spline_mode="cubic"):

    """
    :param dataset1:        the dataset whose energy axis is to be interpolated to that of dataset2
    :param dataset2:        dataset providing the energy axis used to interpolate dataset1 to
    :param spline_mode:     the mode applied to calculate the spline
    :return:
    """

    nu_other = dataset2.index.values

    nu_this = dataset1.index.values
    tau_this = dataset1.columns.values
    dod_this = dataset1.to_numpy()

    # create a grid interpolation function using uncorrupted data points
    f = interp2d(tau_this, nu_this, dod_this, kind=spline_mode)


    testout = f(tau_this, nu_other)
    print(dataset1.shape)
    print(testout.shape)

    # use this function to re-interpolate to the initial grid and parse into DataFrame
    interpolated_onto_ref_nu_axis = pd.DataFrame(f(tau_this, nu_other), index=nu_other, columns=tau_this)

    return interpolated_onto_ref_nu_axis
