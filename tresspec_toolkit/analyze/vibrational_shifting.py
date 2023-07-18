import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from tresspec_toolkit.process.trim_dataset_rev import trim_dataset_rev as trim_dataset
from scipy.optimize import minimize_scalar


def vibrational_shifting(data, spectral_ranges=[[-np.inf, np.inf]],
                         time_ranges=[[-np.inf, np.inf]], degree=5, window_size=7, plot=False):

    """

    :param data:            the data provided as a pandas DataFrame
    :param spectral_ranges: the spectral range(s) where to search for shifting bands
    :param time_ranges:     the time range(s) to take into consideration for this analysis
    :param degree:          the degree of the polynomial that is fitted to the data (whose root are determined)
    :param window_size:     the number of points to the left and to the right relative to the absolute maximum of a
                            given spectrum
    :return:
    """

    data = trim_dataset(data, spectral_ranges=spectral_ranges, time_ranges=time_ranges)

    peak_maximum = list()
    peak_maximum2 = list()

    for delay, spectrum in data.iteritems():
        idx_lb, idx_ub = spectrum.argmax() - window_size, spectrum.argmax() + window_size + 1

        print(f"Maximum found at {spectrum.idxmax()} cm**-1")

        x = data.index[idx_lb: idx_ub]
        y = spectrum.iloc[idx_lb: idx_ub]

        # fit a polynomial to the data
        pp = np.polynomial.polynomial.polyfit(x, y, 5)

        # build a polynomial function from the coefficient of the fitted polynomial (method 1)
        polynomial = np.poly1d(np.flipud(pp))

        # minimize the polynomial in the given range of interest
        fit = minimize_scalar(-polynomial, bounds=(min(x), max(x)),
                              method='bounded')

        # calculate roots of the polynomial (method 2)
        roots = np.roots(polynomial.deriv())
        index = (np.abs(roots-spectrum.idxmax())).argmin()
        from_polynomial = roots[index]

        # parse into lists
        peak_maximum.append(from_polynomial.real)
        peak_maximum2.append(fit.x)

        if plot:
            fig, ax = plt.subplots()
            ax.plot(x, y, marker="o")
            ax.plot(x, np.polynomial.polynomial.polyval(x, pp), marker="o")
            ax.plot(x, polynomial(x))
            ax.axvline(spectrum.idxmax(), color="k", alpha=0.2)
            ax.axvline(from_polynomial, color="k", alpha=0.2, linestyle="dotted")
            ax.axvline(fit.x, color="k", alpha=0.2, linestyle="dashed")


    fig, ax = plt.subplots()
    ax.plot(data.columns, np.array(peak_maximum), marker="o")
    ax.plot(data.columns, np.array(peak_maximum2), marker="o")

    peak_maximum = pd.DataFrame(peak_maximum, index=data.columns)

    return peak_maximum
