from scipy.linalg import lstsq
import numpy as np


def intensity_scaling(df1, beta):

    """

    :param df1:         the dataset to be scaled
    :param beta:        optional argument; coefficients of the linear scaling (otherwise determined automatically)
    :return:
    """

    df1_scaled = df1 * beta[0] + np.ones_like(df1) * beta[1]

    return df1_scaled


import pandas as pd

y = np.arange(0, 20, 1).reshape(10, 2)
y = pd.DataFrame(y)
x = y + 0.25 * np.random.randn(y.shape[0], y.shape[1])


out21 = intensity_scaling(x, beta=[2, 4])
