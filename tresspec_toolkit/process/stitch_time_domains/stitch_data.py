import numpy as np
import pandas as pd
from scipy.interpolate import interp2d
from scipy.optimize import minimize
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from scipy.linalg import lstsq

from tresspec_toolkit.misc.determine_linear_scaling import *
from tresspec_toolkit.misc.intensity_scaling import *
from tresspec_toolkit.misc.interpolate_to_new_frequency_axis import *


def determine_frequency_shift(df1, ref, df1_idx, ref_idx,  delta_lambda):
    df1_interpolated = interpolate_to_new_frequency_axis(df1, ref, delta_lambda)
    _, rmse = determine_linear_scaling(df1_interpolated.iloc[:, df1_idx], ref.iloc[:, ref_idx])

    return rmse


def stitch_data(data1, data2, frequency_shift=None, common_delay_points=None, create_plots=True):

    if common_delay_points is None:
        print("Auto-detect data that are present in both datasets...")

        common_delays = np.intersect1d(data1.columns, data2.columns)

        df1_col_idx = [data1.columns.get_loc(delay) for delay in common_delays]  # to create pointer list containing the respective indices
        df2_col_idx = [data2.columns.get_loc(delay) for delay in common_delays]  # to create pointer list containing the respective indices
    else:
        df1_col_idx = [i for i in range(data1.shape[1]-common_delay_points, data1.shape[1])]
        df2_col_idx = [i for i in range(common_delay_points)]

    ####################################################################################################################
    # if no value provided for offset of frequency axis, here we'll determine it automatically
    if frequency_shift is None:
        print("Invoke automatic determination of frequency shift")
        res = minimize((lambda shift: determine_frequency_shift(data2, data1,
                                                                df2_col_idx, df1_col_idx,
                                                                shift)),
                       x0=np.array([0.5]), method="SLSQP")
        frequency_shift = res.x[0]
        print(f"\nAutomatic detection of frequency shift successful!")
        print(f"Detected a wavelength shift of data2 by {res.x[0]} nm")
        print(f"Adjust frequency axis of 'data2' using this value to align the two datasets.\n")

    ####################################################################################################################

    # interpolating data2 to nes frequency axis
    data2_interpolated = interpolate_to_new_frequency_axis(data2, data1, frequency_shift)

    # determine scaling factor and offset to match both sets of data
    beta, _ = determine_linear_scaling(data2_interpolated.iloc[:, df2_col_idx],
                                       data1.iloc[:, df1_col_idx])

    # apply the previously determined scaling factor + offset to match data
    data2_interpolated_and_scaled = intensity_scaling(data2_interpolated, beta)

    ################################################################################################################
    # make a figure to visualize the results of this algorithm
    if create_plots:
        fig, axs = plt.subplots(3, 1, sharex=True)
        fig.subplots_adjust(wspace=0.03)
        axs[0].plot(data1.index, data1.iloc[:, df1_col_idx], marker="o", label="data_1")
        axs[0].plot(data2.index, data2.iloc[:, df2_col_idx], marker="o", label="data_2")
        axs[0].legend(frameon=False, loc="lower left", bbox_to_anchor=(1.04, 0.5))

        axs[1].plot(data1.index, data1.iloc[:, df1_col_idx], label="data_1")
        axs[1].plot(data2_interpolated_and_scaled.index, data2_interpolated_and_scaled.iloc[:, df2_col_idx],
                    label="data_2 (interpolated and shifted)")
        axs[1].legend(frameon=False, loc="lower left", bbox_to_anchor=(1.04, 0.5))

        axs[2].plot(data1.index, data2_interpolated_and_scaled.iloc[:, df2_col_idx] - data1.iloc[:, df1_col_idx],
                    label="residuals")
        axs[2].legend(frameon=False, loc="lower left", bbox_to_anchor=(1.04, 0.5))

        axs[2].set_xlabel("wavenumber / cm$^{-1}$")
        for ax in axs:
            ax.axhline(color="k", alpha=0.2)
    ####################################################################################################################
    merged = pd.concat((data1, data2_interpolated_and_scaled), axis=1)

    return merged, data2_interpolated_and_scaled
