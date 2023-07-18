import numpy as np
import pandas as pd
import os
import glob


def uv_pump_mir_probe_dual_solstice(wrkpath, discard_stitching_blocks=[], load_processed_data=True, zero_step=7,
                                    time_increment=11.83, time_axis_in="ns"):

    """
    invoke uv_pump_mir_probe_dual_solstice to load data recorded on the UV-pump-mIR-probe experiment with a dual
    solstice configuration

    :param wrkpath:                     the path containing the *sve.csv files as received from the spectrometer
    :param discard_stitching_blocks:    a list containing the indices of bad stitching blocks which are to be discarded
    :param load_processed_data:         boolean whether to use preprocessed data if there are any found on the disk
    :param zero_step:                   the step in which the pump and probe pulses are reaching the sample
                                        simultaneously
    :param time_increment:              the time increment between steps
    :param time_axis_in:                string, e.g. "ns" or "ps"


    :return:
        - runs:                         a list containing the individual measurements
        - runs_sb:                      a list of the individual measurements separated into their stitching blocks
    """

    print(f"Time axis containing delays in '{time_axis_in}'")
    if time_axis_in == "ps":
        time_increment *= 1000
    elif time_axis_in == "micros" or time_axis_in == "µs":
        time_increment *= 1e-3
    else:
        time_increment *= 1


    if bool(discard_stitching_blocks):
        print("discarding stitching runs ...", discard_stitching_blocks)

    if type(discard_stitching_blocks) != list:
        discard_stitching_blocks = [discard_stitching_blocks]

    # convert list to numpy array, make sure that all values are integers and lower by one for following handling
    discard_stitching_blocks = np.array(discard_stitching_blocks).astype(int) - 1

    ############################################
    #                                          #
    # function to read data from a single file #
    #                                          #
    ############################################

    def loaduvmirdata(working_path, bad_sb):
        data = np.loadtxt(working_path)
        rows, cols = data.shape

        # extract number of runs, delays, stitching blocks and pixels
        no_scans = np.count_nonzero((data == data[0, :]).all(axis=1))
        no_delays = int(rows / no_scans - 1)
        no_sb = np.count_nonzero(np.diff(data[0, 1:]) > 0) + 1
        no_pixels = int((cols - 1) / no_sb)

        # create a list storing the individual stitching blocks
        scans_sb = list()
        for i in range(no_scans):
            lower_index = i * no_delays + (i + 1)
            upper_index = (i + 1) * no_delays + i

            scans_sb_child = list()
            for k in range(no_sb):
                if k not in bad_sb:
                    # identify independent and dependent variables
                    wavelengths_sb = data[lower_index - 1, k * no_pixels + 1: (k+1) * no_pixels + 1]
                    delays_sb = (data[lower_index:upper_index + 1, 0] - zero_step) * time_increment
                    data_sb = data[lower_index:upper_index + 1, k * no_pixels + 1: (k+1) * no_pixels + 1]

                    # parse into pandas DataFrame
                    df_sb = pd.DataFrame(data_sb, columns=wavelengths_sb, index=delays_sb)

                    df_sb = df_sb.sort_index(axis=0)

                    # append to temporary list
                    scans_sb_child.append(df_sb)

            # append child list to parent list
            scans_sb.append(scans_sb_child)

        # compile good stitching blocks into DataFrames
        scans = list()
        for i in range(no_scans):

            scan_filtered = pd.concat(scans_sb[i], axis=1)

            wn = 10**7 / scan_filtered.columns.to_numpy()
            delays = scan_filtered.index.to_numpy()

            # create DataFrame and sort frequency axis in ascending order
            df = pd.DataFrame(scan_filtered.to_numpy().transpose(), index=wn, columns=delays)
            df = df.sort_index(axis=0)
            df = df.sort_index(axis=1)

            # append to list of measurements
            scans.append(df)

        return scans, scans_sb

    #########################################################################
    #                                                                       #
    #    final code to load the data, either from directory or from file    #
    #                                                                       #
    #########################################################################
    if os.path.isfile(os.path.join(os.getcwd(), "processed_data\denoised_data_sve.dat")) and load_processed_data:
        print("Processed data found on disk. Loading...")

        pth_cleared_data = os.path.join(os.getcwd(), "processed_data\denoised_data_sve.dat")

        runs, runs_sb = loaduvmirdata(pth_cleared_data, discard_stitching_blocks)

    else:
        print("No processed data found on disk or user requested reloading of raw data. Loading...")
        if os.path.isdir(wrkpath):
            files = glob.glob(wrkpath + "/**/*_sve.dat", recursive=True)

            # initialization
            counter = 0
            tmp = list()
            tmp_sb = list()

            for file in files:
                runs_tmp, runs_sb_tmp = loaduvmirdata(file, discard_stitching_blocks)

                tmp.append(runs_tmp)
                tmp_sb.append(runs_sb_tmp)
                counter += 1

            runs = list()
            runs_sb = list()

            for n in range(len(tmp)):
                for m in range(len(tmp[n])):
                    runs.append(tmp[n][m])
                    runs_sb.append(tmp_sb[n][m])

        elif os.path.isfile(wrkpath):
            runs, runs_sb = loaduvmirdata(wrkpath, discard_stitching_blocks)

    return runs, runs_sb
