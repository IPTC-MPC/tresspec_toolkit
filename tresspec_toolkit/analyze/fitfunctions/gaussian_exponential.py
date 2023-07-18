import numpy as np


def gaussian_exponential(t, a0, a1, tau1, a2, tau2):
    y = a0 + a1 * np.exp(-t**2/tau1**2) + a2 * np.exp(-t/tau2)
    return y
