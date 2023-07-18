import numpy as np


def biexponential(t, a1, tau1, a2, tau2, y0):
    y = a1 * np.exp(-t/tau1) + a2 * np.exp(-t/tau2) + y0
    return y
