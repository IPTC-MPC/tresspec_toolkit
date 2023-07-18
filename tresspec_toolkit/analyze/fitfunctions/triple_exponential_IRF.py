import numpy as np
from scipy.special import erf


def triple_exponential_irf(t, a0, a1, tau1, a2, tau2, a3, tau3, fwhm, t0):
    """
    :param t:       time axis
    :param a0:      amplitude of constant offset
    :param a1:      amplitude of first component
    :param tau1:    time constant of first component
    :param a2:      amplitude of second component
    :param tau2:    time constant of second component
    :param a3:      amplitude of third component
    :param tau3:    time constant of third component
    :param fwhm:    FWHM of the IRF (determined by temporal resolution of experiment)
    :return:
    """
    tau_inf = 10**6
    sigma = fwhm/(2*np.sqrt(2*np.log(2)))

    # comp1 = a1 * np.exp(t/tau1 + sigma**2/(2*tau1**2)) * (1+erf((t*tau1-sigma**2)/(np.sqrt(2)*sigma*tau1)))

    # print(comp1)
    # comp2 = a2 * np.exp(t/tau2 + sigma**2/(2*tau2**2)) * (1+erf((t*tau2-sigma**2)/(np.sqrt(2)*sigma*tau2)))
    # print(comp2)

    # comp3 = a3 * np.exp(t/tau3 + sigma**2/(2*tau3**2)) * (1+erf((t*tau3-sigma**2)/(np.sqrt(2)*sigma*tau3)))
    # print(comp3)

    y = 0.5 * (a1 * np.exp(-(t-t0)/tau1 + sigma**2/(2*tau1**2)) * (1+erf(((t-t0)*tau1-sigma**2)/(np.sqrt(2)*sigma*tau1))) +
               a2 * np.exp(-(t-t0)/tau2 + sigma**2/(2*tau2**2)) * (1+erf(((t-t0)*tau2-sigma**2)/(np.sqrt(2)*sigma*tau2))) +
               a3 * np.exp(-(t-t0)/tau3 + sigma**2/(2*tau3**2)) * (1+erf(((t-t0)*tau3-sigma**2)/(np.sqrt(2)*sigma*tau3))) +
               a0 * (1+erf(((t-t0)/(np.sqrt(2)*sigma)))))

    return y
