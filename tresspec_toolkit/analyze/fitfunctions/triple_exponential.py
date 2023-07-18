import numpy as np


def triple_exponential(t, a1, tau1, a2, tau2, a3, tau3, y0):
    y = a1 * np.exp(-t/tau1) + a2 * np.exp(-t/tau2) + a3 * np.exp(-t/tau3) + y0
    return y
