import numpy as np
import math
import copy
from scipy.stats import median_abs_deviation
import matplotlib.pyplot as plt


def outliers_median_filter(datasets, window_size=3, threshold=3.0, plot=False, pad_mode="edge"):
    """
    outlier_median_filter removes spikes in datasets due to corrupted data points (outliers) via a median filtering
    approach.

    :param datasets:        the data that are to be filtered provided as pandas DataFrame (or a list thereof)
    :param window_size:     the size of the window used for the filtering
    :param threshold:       the threshold above which the filtering shall take effect
    :param plot:            a boolean parameter whether to plot the results or not
    :param pad_mode:        mode how to pad the data above its edges
    :return:
    """

    # make sure window size is odd
    window_size = 2 * math.floor(window_size / 2) + 1

    pad_size = int((window_size - 1) / 2)

    # make sure data are provided as list
    if not isinstance(datasets, list):
        datasets = [datasets]

    data_corrected_out = list()

    for data in datasets:
        # pad zeros

        try:
            data_padded = np.pad(data, pad_size, mode=pad_mode)
        except ValueError:
            print("Specified pad_mode is invalid. Using default 'edge' mode...")
            data_padded = np.pad(data, pad_size, mode="edge")

        # creating a copy
        data_median = np.zeros_like(data)

        data_corrected = copy.deepcopy(data)

        # loop over the points
        for i in range(pad_size, data.shape[0] + pad_size):
            for j in range(pad_size, data.shape[1] + pad_size):

                kernel = data_padded[i - pad_size:i + pad_size + 1,
                                     j - pad_size:j + pad_size + 1]

                median = np.median(np.ndarray.flatten(kernel))

                data_median[i - pad_size, j - pad_size] = median

                mad = median_abs_deviation(np.ndarray.flatten(kernel))

                if abs(data.iloc[i - pad_size, j - pad_size] - median) > abs(threshold * mad):
                    data_corrected.iloc[i - pad_size, j - pad_size] = median

        # calculate residuals
        residuals = data_corrected - data

        if plot:
            # make figures
            fig, ax = plt.subplots(1, 3, figsize=(18, 6), sharey=True)

            ax[0].set_title("Raw Data")
            ax[1].set_title("Median Filtered Data")
            ax[2].set_title("Residuals of filter")

            # create contour plots to visualize results of algorithm
            levels = np.linspace(-data.abs().to_numpy().max(), data.abs().to_numpy().max(), 1000)
            ax[0].contourf(data.index, data.columns, data.T, levels=levels, cmap="seismic")

            levels = np.linspace(-data_corrected.abs().to_numpy().max(), data_corrected.abs().to_numpy().max(), 1000)
            ax[1].contourf(data_corrected.index, data_corrected.columns, data_corrected.T, levels=levels, cmap="seismic")

            levels = np.linspace(-residuals.abs().to_numpy().max(), residuals.abs().to_numpy().max(), 1000)
            ax[2].contourf(residuals.index, residuals.columns, residuals.T, levels=levels, cmap="seismic")

        # appending to output variable
        data_corrected_out.append(data_corrected)

    return data_corrected_out
