import numpy as np


def exponential(t, a1, tau1, y0):
    y = a1 * np.exp(-t/tau1) + y0
    return y
