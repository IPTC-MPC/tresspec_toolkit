import numpy as np
import pandas as pd
from tresspec_toolkit.simulate.lognormal import *
from tresspec_toolkit.simulate.gaussian import *


def simulate_dod(nu, t, gaussian_parameters, lognormal_parameters, tau=10, noise_level=0.0):
    """
    A function used to generate a dummy data matrix as could be returned from a measurement
    (especially handy for testing and development purposes)

    :param nu:                      the frequency axis
    :param t:                       the delay axis
    :param gaussian_parameters:     the parameters of the gaussian shaped transient bleach (amplitude, nu0, sigma, y0)
    :param lognormal_parameters:    the parameters of the lognormal shaped transient absorption
                                    (amplitude, nu0, delta, rho)
    :param tau:                     the decay constant of the simulated signal
    :param noise_level:             scaling factor to add white noise

    :return:                        a data matrix
    """

    spectrum = lognormal(nu, *lognormal_parameters) - gaussian(nu, *gaussian_parameters)
    decay = np.exp(-t/tau)

    # creating the dummy data
    dummy_data = np.atleast_2d(spectrum).T @ np.atleast_2d(decay) + noise_level * np.random.randn(len(nu), len(t))
    dummy_data = pd.DataFrame(dummy_data, index=nu, columns=t)

    return dummy_data
