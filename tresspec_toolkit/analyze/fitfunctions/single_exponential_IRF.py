import numpy as np
from scipy.special import erf

def single_exponential_irf(t, a0, a1, tau1, fwhm, t0):
    """

    :param t:       time axis
    :param a0:      amplitude of constant offset
    :param a1:      amplitude of first component
    :param tau1:    time constant of first component
    :param a2:      amplitude of second component
    :param tau2:    time constant of second component
    :param a3:      amplitude of third component
    :param tau3:    time constant of third component
    :param sigma:   characteristic
    :return:
    """

    tau_inf = 10**10
    sigma = fwhm/(2*np.sqrt(2*np.log(2)))

    comp1 = a1 * np.exp(-t/tau1 + sigma**2/(2*tau1**2)) * (1+erf((t*tau1-sigma**2)/(np.sqrt(2)*sigma*tau1)))
    print(f"componennt 1 = {comp1}")
    comp2 = a0 * np.exp(-t/tau_inf + sigma**2/(2*tau_inf**2)) * (1+erf((t*tau_inf-sigma**2)/(np.sqrt(2)*sigma*tau_inf)))
    print(f"component 2 = {comp2}")

    y = 0.5 * (a1 * np.exp(-(t-t0)/tau1 + sigma**2/(2*tau1**2)) * (1+erf(((t-t0)*tau1-sigma**2)/(np.sqrt(2)*sigma*tau1))) +
               a0 * np.exp(-(t-t0)/tau_inf + sigma**2/(2*tau_inf**2)) * (1+erf(((t-t0)*tau_inf-sigma**2)/(np.sqrt(2)*sigma*tau_inf))))

    return y