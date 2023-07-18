import numpy as np


def gaussian(nu, a, nu0, sigma, y0):
    return a * np.exp(-((nu - nu0) / sigma) ** 2) + y0

