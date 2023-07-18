import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import glob
import time


def series_of_ir_spectra(pth, pth_ref=None, timescale="min", recalculate=False, dismiss_explicit=[], dismiss_range=[],
                         dismiss_cutoff=np.inf, spectral_range=[-np.inf, np.inf], time_range=[-np.inf, np.inf],
                         save_data=True,
                         troubleshoot=False):
    """
    Invoke series_of_ir_spectra to load a time series of FTIR spectra for investigation of long term trends in the IR
    spectrum.

    :param pth:             path to directory containing "/dynamic/" directory that stores the spectra
    :param pth_ref:         if required the reference spectrum (usually the solvent)
    :param timescale:       time scale of the experiment ("s", "min", "h")
    :param recalculate:     boolean whether to recalculate data although old processed data are detected
    :param dismiss_explicit: indices of bad measurements to be excluded
    :param dismiss_range:    array containing lower and upper indices of blocks of bad data that are to be rejected
    :param dismiss_cutoff:   limit up to which data are to be taken account, data exceeding this index or omitted
    :param spectral_range:   array storing the lower and upper limit of the spectral window to be considered
    :param time_range:       array storing the lower and upper limit of the time range to be considered
    :param save_data:       boolean whether to save data or not
                            (defaults to "True", data stored in "od.csv" and "dod.csv", respectively)
    :param troubleshoot:    boolean to activate printing when facing problems with script

    :return: data_dod:      the DataFrame containing the data in terms of differential optical densities
                            (referenced against very first spectrum defining t0)
             data_od:       the DataFrame containing the data in terms of optical densities
                            (referenced against an external reference (usually the solvent))
    """

    # make sure data are in sorted format
    spectral_range = np.array(spectral_range)
    time_range = np.array(time_range)

    ######################################################################
    #                     difference spectra (in dOD)                    #
    ######################################################################

    if os.path.isfile(os.path.join(pth, "dod.csv")) and not recalculate:
        print("Found calculated difference spectra in file 'dod.csv'. Loading...")
        data_dod = pd.read_csv(os.path.join(pth, "dod.csv"), sep="\t", index_col=0, dtype=float)
        data_dod.columns = data_dod.columns.astype(float)
    else:
        print("No file 'dod.csv' detected or user requested recalculation. Calculating spectra from scratch...")
        dismiss_explicit = np.array(dismiss_explicit)
        if bool(dismiss_range):
            for i in range(int(len(dismiss_range) / 2)):
                # append indices to list storing indices of measurements to be rejected
                dismiss_explicit = [*dismiss_explicit,
                                    *[y for y in range(dismiss_range[2 * i], dismiss_range[2 * i + 1] + 1)]]

        # setting time scale of measurement
        if timescale == "min":
            t_div = 60
        elif timescale == "sec":
            t_div = 1
        elif timescale == "h":
            t_div = 3600

        # creating list of files
        files = glob.glob(os.path.join(pth, "dynamic/*.csv"))
        files.sort(key=os.path.getmtime)

        if troubleshoot:
            print(files)

        ###########################
        #    loop to load data    #
        ###########################
        dates = list()

        for idx, file in enumerate(files):
            if idx + 1 == dismiss_cutoff:
                break
            elif idx+1 in dismiss_explicit:
                print("Rejecting measurement No. ", idx+1)
                continue
            else:
                tmp = np.loadtxt(os.path.join(pth, 'dynamic', file), delimiter=';')
                dates.append(os.path.getmtime(os.path.join(pth, 'dynamic', file)))

                if idx == 0:
                    intensity = tmp[:, 1]
                    frequency_axis = tmp[:, 0]
                else:
                    intensity = np.column_stack((intensity, tmp[:, 1]))

        # determine effective number of delays for subsequent initialization of I0 matrix
        _, no_delays = intensity.shape

        # creating matrix with I_t0 for subsequent calculation of Delta OD
        intensity_t0 = np.tile(intensity[:, 0], (no_delays, 1)).transpose()

        ######################################################################
        #    calculate spectra in terms of differential optical densities    #
        ######################################################################
        dod = np.log10(intensity_t0 / intensity)

        # Todo: implement sanity check to verify that all frequency axes are identical
        dates = np.array(dates)
        delays = (dates - dates[0]) / t_div

        data_dod = pd.DataFrame(dod, index=frequency_axis, columns=delays)

        #########################################################
        #    save calculated spectra to *.csv files             #
        #########################################################
        if save_data:
            data_dod.to_csv(os.path.join(pth, "dod.csv"), sep="\t")
            print("Difference spectra stored in file 'dod.csv'")

    ######################################################################
    #                     absorption spectra (in OD)                     #
    ######################################################################

    if os.path.isfile(os.path.join(pth, "od.csv")) and not recalculate:
        print("Found calculated spectra in file 'od.csv'. Loading...")
        data_od = pd.read_csv(os.path.join(pth, "od.csv"), sep="\t", index_col=0, dtype=float)
        data_od.columns = data_od.columns.astype(float)
    else:
        if pth_ref is not None:
            print("No file 'od.csv' detected or user requested recalculation. Calculating spectra from scratch...")
            #########################################################
            #    calculate spectra in terms of optical densities    #
            #########################################################
            data_od = np.nan

            if os.path.isfile(pth_ref):
                print("Background spectrum found...")
                tmp_ref = np.loadtxt(pth_ref, delimiter=';')

                # compile array for matrix calculation
                intensity_ref = np.tile(tmp_ref[:, 1], (no_delays, 1)).transpose()

            if 'intensity_ref' in locals():
                od = np.log10(intensity_ref/intensity)

                data_od = pd.DataFrame(od, index=frequency_axis, columns=delays)

            #########################################################
            #    save calculated spectra to *.csv file              #
            #########################################################
            if save_data:
                data_od.to_csv(os.path.join(pth, "od.csv"), sep="\t")
                print("Absorption spectra stored in file 'dod.csv'")

    ######################################################################
    #     trimming dataset to delays and spectral range of interest      #
    ######################################################################

    data_dod = data_dod.iloc[(data_dod.index >= min(spectral_range)) & (data_dod.index <= max(spectral_range)),
                             (data_dod.columns >= min(time_range)) & (data_dod.columns <= max(time_range))]
    if pth_ref is None:
        data_od = None
    else:
        data_od = data_od.iloc[(data_od.index >= min(spectral_range)) & (data_od.index <= max(spectral_range)),
                               (data_od.columns >= min(time_range)) & (data_od.columns <= max(time_range))]

    return data_dod, data_od
