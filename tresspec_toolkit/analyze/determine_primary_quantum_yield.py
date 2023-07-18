import pandas as pd
import numpy as np


def determine_primary_quantum_yield(data, nu, t_ref=0, av_delays=4):

    """
    A little function that allows a quick estimation of the primary quantum yield by calculating the ratio of the signal
    intensities at zero delay and "infinite" delay (i.e. large delays)

    :param data:        the data provided as a pandas DataFrame
    :param nu:          the reference frequency. The signal strengths at this spectral position will be used for the
                        following estimation
    :param t_ref:       the delay that is regarded as delay zero
                        (usually 0.0, change only if there is a good argument to do so)
    :param av_delays:   the number of delays at late delay times that are averaged together for numerically more
                        reliable estimate
    :return:            quantum_yield: the primary quantum yield of the photophysical/photochemical experiment
    """

    dod0 = float(data.iloc[abs(data.index - nu) == min(abs(data.index - nu)),
                           abs(data.columns - t_ref) == min(abs(data.columns - t_ref))].values)

    print(f"dmOD(t = 0): {dod0}")
    dod_inf = float(data.iloc[abs(data.index - nu) == min(abs(data.index - nu)), -av_delays:].mean(axis=1))
    print(f"dmOD(t = inf): {dod_inf}")

    quantum_yield = dod_inf/dod0

    print(f"Quantum Yield: {np.around(quantum_yield*100, decimals=1)}%")

    return quantum_yield
