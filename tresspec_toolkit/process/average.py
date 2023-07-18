import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def average(data, dismiss=[], std_averaging=False, baseline_range=None, delays=[-np.inf, np.inf], signal=None):

    """
    Invoke this function to averaged together a compilation of transient spectra

    :param data:            the data provided as a list of pandas Dataframes
    :param dismiss:         a list containing the indices of the measurements to be excluded from the averaging
    :param std_averaging:   boolean whether to apply weighting based on the signal-to-noise ratio of the individual
                            measurements
    :param baseline_range:  a list containing the range of the baseline (required in the determination of the SNR if
                            std_averaging is desired)
    :param delays:          delays used for the std_averaging procedure
    :param signal:          the spectral position of the signal (required for determination of the SNR)
    :return:                the averaged data based on the provided input data
    """

    if baseline_range is not None:
        baseline_range.sort()
    delays.sort()

    if not isinstance(dismiss, list):
        dismiss = [dismiss]

    # identify which dataset to use for checking time and frequency axis for consistency
    pointer = 0
    if dismiss:
        while pointer in dismiss:
            pointer += 1

    # paste into numpy array and shift by one (to account for list indexing in python)
    if dismiss:
        dismiss = np.array(dismiss) - 1
        print('Number of dismissed measurements for averaging: ', len(dismiss))
        print('Effective number of measurements for averaging: ', len(data) - len(dismiss))

    ###############################
    #    set weighting factors    #
    ###############################
    if std_averaging:
        print("applying averaging based on signal-to-noise ratio of the individual measurements ...")
        snr = list()
        for idx, scan in enumerate(data):
            if idx in dismiss:
                snr.append(0)
            else:
                noise = scan.iloc[(scan.index >= baseline_range[0]) & (scan.index <= baseline_range[1]),
                                  (scan.columns >= delays[0]) & (scan.columns <= delays[1])].std()

                sig = scan.iloc[(scan.index >= signal - 5) & (scan.index <= signal + 5),
                                (scan.columns >= delays[0]) & (scan.columns <= delays[1])].abs().max()

                snr.append((sig / noise).mean())

        weighting_factors = np.array(snr) / sum(np.array(snr))
        print("weighting factors.... = ", weighting_factors)
    else:
        print("averaging data, no weighting involved ...")
        weighting_factors = np.ones(len(data))

        weighting_factors[dismiss] = 0
        weighting_factors = weighting_factors / sum(weighting_factors)
        print("weighting factors.... ", weighting_factors)

    # checking time and frequency axis for consistency
    for idx, run in enumerate(data):
        if idx in dismiss:
            print("Run # ", idx+1, "will be dismissed.")
        else:
            if not (set(data[pointer].columns) == set(run.columns)) or not \
                   (set(data[pointer].index) == set(run.index)):
                print("Time axes and/or Frequency axes are inconsistent. Abort ...")
                break

    # initializing array to store averaged data
    av = np.zeros(data[pointer].shape)

    ##############################
    #                            #
    #    loop to average data    #
    #                            #
    ##############################
    for idx, scan in enumerate(data):
        av = av + weighting_factors[idx] * scan.values

    averaged = pd.DataFrame(av, index=data[pointer].index, columns=data[pointer].columns)
    return averaged
