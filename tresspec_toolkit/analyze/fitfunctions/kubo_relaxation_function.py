import numpy as np


def kubo_relaxation_function(t, delta, gamma):
    # y = [v(t) - v(inf)] / [v(0) - v(inf)]
    y = np.exp(-(delta/gamma) * (np.exp(-gamma * t) + gamma * t - 1))
    return y
