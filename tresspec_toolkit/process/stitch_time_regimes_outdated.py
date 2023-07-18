import numpy as np
import pandas as pd
from tresspec_toolkit.process import find_transients

def stitch_time_regimes(mechanical, electronic, f_sc=1.0, electronic_delay_cutoff=10000, pixel_shift=0,
                        reference_signal=None):

    """

    :param mechanical:              Dataset containing data acquired with mechanical delay line
    :param electronic:              Dataset containing data acquired by electronically delaying the two lasers
    :param f_sc:                    scaling factor applied to the second dataset to account for intensity differences
    :param electronic_delay_cutoff: the threshold below which the data from the second measurement should be ignored
    :return:
    """

    if len(np.setdiff1d(mechanical.index, electronic.index)) > 0:
        print("Warning! The frequency axes are inconsistent. Consider interpolating the on to the other beforehand")

    # shift the datasets one with respect to the other if necessary
    if pixel_shift > 0:  # positive pixel shift
        mechanical = mechanical.iloc[:(-pixel_shift), :]
        electronic = electronic.iloc[pixel_shift:, electronic.columns > electronic_delay_cutoff]
    elif pixel_shift < 0:
        mechanical = mechanical.iloc[abs(pixel_shift):, :]
        electronic = electronic.iloc[:-abs(pixel_shift), electronic.columns > electronic_delay_cutoff]
    else:
        electronic = electronic.iloc[:, electronic.columns > electronic_delay_cutoff]

    # reset frequency axis of electronically delayed spectra
    electronic.index = mechanical.index

    # automatic determination of scaling factor
    if reference_signal is not None:
        print(f"Reference signal provided: {reference_signal}")
        print(f"Using this signal to determine scaling factor automatically")

        mechanical_reference = find_transients(mechanical, take_traces_at=reference_signal)
        electronic_reference = find_transients(electronic, take_traces_at=reference_signal)

        f_sc = np.mean(mechanical_reference.iloc[0, -5:])/np.mean(electronic_reference.iloc[0, :5])
        print(f"determined scaling factor: {f_sc}")

    # delay axis
    delays = np.concatenate((mechanical.columns.values, electronic.columns.values))

    # concatenated datasets
    merged = np.concatenate((mechanical.to_numpy(), f_sc * electronic.to_numpy()), axis=1)
    merged = pd.DataFrame(merged, index=mechanical.index, columns=delays)

    return merged
