import numpy as np
import pandas as pd
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt


def calculate_product_spectra_LD(dataset, stationary_ir, nu_sc=1.0, nu_shift=0.0, width_convolution=2.5, f_sc=None,
                                 plot=False):

    """
    :param dataset:             the dataset(s) containing the data from the time-resolved experiment (either a pandas
                                DataFrame or list thereof)
    :param stationary_ir:       the stationary IR spectrum
    :param nu_sc:               scaling factor to be applied to frequency axis
    :param nu_shift:            constant shift of frequency axis
    :param width_convolution:   width of convolution
    :param f_sc:                scaling factor to scale the stationary spectrum to the pump-probe spectrum
    :return:
    """

    def throw_waring(flag):
        if flag:
            print("WARNING:")
            print("Frequency axis of stationary spectrum does not cover full spectral "
                  "range of time-resolved experiment.")
            print("This may lead to odd behavior due to interpolation.\n")

    print("##########################################################")
    print("#    Calculation of Purely Absorptive Product Spectra    #")
    print("##########################################################")
    print("")

    throw_waring(min(stationary_ir.index) > min(dataset.index))

    # load stuff
    wavenumber_final_cm = dataset.index  # frequency axis of the time-resolved experiment

    if stationary_ir["OD"].isnull().values.any():
        print("Found NaNs in stationary spectrum, trimming spectrum to spectral range of interest")
        stationary_ir = stationary_ir.iloc[(stationary_ir.index >= min(dataset.index) - 10) &
                                           (stationary_ir.index <= max(dataset.index) + 10), :]

    ####################################################################################################################
    # interpolate to have both datasets on the same scale
    cs = CubicSpline(nu_sc * stationary_ir.index - nu_shift, stationary_ir.OD, bc_type='natural')

    # interpolate the stationary spectrum to the frequency scale of the time resolved experiment
    linear_od = cs(dataset.index)

    # normalization to the maximum
    linear_od = linear_od / max(linear_od)

    # Convolution is needed for subtraction if line widths of linear FTIR and pump-probe spectra are different.
    time_axis_convolution = np.arange(-100, 101, 1)

    # gaussian function used to convolve the stationary spectrum with
    go = np.exp(-time_axis_convolution**2 / width_convolution**2)

    # convolve
    c = np.convolve(linear_od, go)

    # concentrate on the relevant range
    interpolated_convolved_linear_ftir = c[100:-100]

    maximum_conv_lin_OD = max(interpolated_convolved_linear_ftir)

    # determine scaling factor if not set explicitly
    if f_sc is None:
        f_sc = min(dataset.loc[:, 0])
        print(f"Automatically determined scaling factor: {f_sc}")

    ####################################################################################################################
    # figure to visualize output
    if plot:
        fig, ax = plt.subplots()
        ax.plot(wavenumber_final_cm, linear_od, label="measured FTIR spectrum")
        ax.plot(wavenumber_final_cm, interpolated_convolved_linear_ftir / maximum_conv_lin_OD,
                label="after convolution", color='r')
        ax.legend()

        fig, ax = plt.subplots()
        ax.plot(dataset.index, dataset.loc[:, 0], label="pump-probe spectrum (0.0 ps)")
        ax.plot(wavenumber_final_cm, f_sc * interpolated_convolved_linear_ftir / maximum_conv_lin_OD,
                label="stationary spectrum (scaled, inverted, convoluted)")
        ax.plot(wavenumber_final_cm, dataset.loc[:, 0] - f_sc * interpolated_convolved_linear_ftir / maximum_conv_lin_OD,
                label="purely absorptive product spectrum")

        ax.axhline(0, color="k", alpha=0.3)

        ax.legend(frameon=False, labelcolor='linecolor', handlelength=0.0)

    # calculate purely absorptive product spectra
    stat = np.atleast_2d(interpolated_convolved_linear_ftir / maximum_conv_lin_OD).T

    convoluted_stationary_spectrum = f_sc * interpolated_convolved_linear_ftir / maximum_conv_lin_OD

    convoluted_stationary_spectrum = pd.DataFrame(convoluted_stationary_spectrum, index=dataset.index)

    paps = dataset - f_sc * np.repeat(stat, dataset.shape[1], axis=1)



    # off that's it

    #stationary_ir = stationary_ir.iloc[(stationary_ir.index >= min(dataset.index)) &
    #                                   (stationary_ir.index <= max(dataset.index)), :]

    ##########################################################################################
    #    calculate natural cubic spline polynomials                                          #
    #    (to project stationary spectrum onto frequency axis of time-resolved experiment)    #
    ##########################################################################################
    #cs = CubicSpline(stationary_ir.index, stationary_ir.OD, bc_type='natural')

    # determine the scaling factor used to fit the intensity of the stationary spectrum to the time-resolved data
    #f_sc = min(dataset.loc[:, 0]) / max(stationary_ir.OD)

    #print(f"Scaling stationary IR spectrum by a factor of {f_sc} ...")


# Todo: at this stage, the fundamental concept seems to be working. However, it might lead to improvement to interpolate
# Todo: the time-resolved dataset instead. We still encounter negative going dips, probably due to insufficient sampling
# Todo: on the frequency axis

    #paps = dataset.to_numpy() - f_sc * np.tile(cs(dataset.index).reshape(len(cs(dataset.index)), 1), dataset.shape[1])

    #paps = pd.DataFrame(paps, index=dataset.index, columns=dataset.columns)
    return paps, convoluted_stationary_spectrum
