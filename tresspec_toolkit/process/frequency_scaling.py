import numpy as np
import pandas as pd
from scipy import stats


def frequency_scaling(data, nu_stat, t_ref=0.0):
    """
    Invoke to calibrate the frequency/wavelength axis of a dataset

    :param data:    the pandas DataFrame storing the data (or a list thereof)
    :param nu_stat: the calibration frequency/wavelength as from i.e. stationary spectra
                    (a list of values can be provided; in this case a linear regression will be applied to set the
                     frequency/wavelength axis)
    :param t_ref:   the delay for which the spectral position of the bleach is definitely set to the calibration values
    :return:        the data as calibrated in the frequency/wavelength domain as a pandas DataFrame (or a list thereof)
    """

    if isinstance(nu_stat, float) or isinstance(nu_stat, int):
        nu_stat = [nu_stat]

    lambda_unscaled = 10**7 / data.index.to_numpy()
    lambda_ref = 10**7 / np.asarray(nu_stat)

    if len(nu_stat) == 1:
        lambda_ref = float(lambda_ref)
        freq_exp = float(data.iloc[:, abs(data.columns - t_ref) == min(abs(data.columns - t_ref))].idxmin(axis=0, skipna=True))

        lambda_exp = 10**7 / freq_exp

        lambda_scaled = lambda_unscaled - (lambda_exp - lambda_ref)
    else:
        freq_exp = np.empty(len(nu_stat))
        for i in range(len(nu_stat)):
            freq_exp[i] = float(data.iloc[(data.index >= nu_stat[i] - 10) & (data.index <= nu_stat[i] + 10),
                                          abs(data.columns - t_ref) == min(abs(data.columns - t_ref))].
                              idxmin(axis=0, skipna=True))

            print('Freq of min: ', freq_exp[i])

        lambda_exp = 10**7 / freq_exp

        slope, intercept, r_value, p_value, std_err = stats.linregress(lambda_exp, lambda_ref)

        lambda_scaled = slope * lambda_unscaled + intercept

    freq_scaled = 10**7 / lambda_scaled
    data_scaled = pd.DataFrame(data.values, index=freq_scaled, columns=data.columns)

    return data_scaled
