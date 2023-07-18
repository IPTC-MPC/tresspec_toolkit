import numpy as np


def lorentzian(nu, nu_0, sigma, i0=1.0):

    """
    Calculate Lorentzian spectral profile

    :param nu:                      the frequency axis
    :param nu_0:                    the center frequency
    :param sigma:                   width of Lorentzian profile
    :param i0:                      the intensity at the maximum (optional, defaults to 1)

    :return:                        a Lorentzian profile
    """

    # function to calculate gaussian broadened TD - DFT spectrum
    intensity = (2 * 100 * i0) / (np.log(10) * np.pi) * sigma / (4 * (nu - nu_0) ** 2 + sigma ** 2)
    return intensity
