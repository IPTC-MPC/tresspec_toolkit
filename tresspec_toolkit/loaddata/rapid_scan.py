import os
import glob
import numpy as np
import pandas as pd


def rapid_scan(pth):

    if os.path.isdir(pth):
        files = glob.glob(pth + "/**/*.dpt", recursive=True)
    elif os.path.isfile(pth):
        files = [pth]

    def construct_time_axis(file_path, dod_mat):
        time_axis_tmp = pd.read_csv(os.path.join(os.path.dirname(file_path), "time_axis.txt"),
                                    delimiter="\t", header=None)

        time_axis = time_axis_tmp.iloc[0, 2:].to_numpy() - time_axis_tmp.iloc[0, 2]

        _, cols = dod_mat.shape

        t_axis_interp = np.append(time_axis, (np.arange(0, (cols - 1) - len(time_axis), 1) + 1)
                                  * np.mean(np.diff(time_axis)) + time_axis[-1])

        return t_axis_interp

    dod = list()
    for file in files:
        data = np.loadtxt(file)
        wn, columns = data.shape
        taxis = construct_time_axis(file, data)

        intensity0 = np.tile(data[:, 1].reshape(wn, 1), columns-1)

        dod.append(pd.DataFrame(np.log10(intensity0/data[:, 1:]), index=data[:, 0], columns=taxis))

    if len(dod) == 1:
        dod = dod[0]

        # try:
        #     time_axis_path = os.path.join(os.path.dirname(file), "time_axis.txt")
        #
        #     time_axis_tmp = pd.read_csv(time_axis_path, delimiter="\t", header=None)
        #
        #
        #     time_axis = time_axis_tmp.iloc[0, 2:].to_numpy() - time_axis_tmp.iloc[0, 2]
        #
        #
        #     t = time_axis
        #     print("everything worked fine")
        # except:
        #     print("Nothing to do")
        #     t = 0
        #     time_axis = os.path.join(os.path.dirname(file), "time_axis.txt")
        #     t = np.loadtxt(time_axis, comments="dStart_time", dtype=float)
        #
        #     t = pd.read_csv(time_axis, sep="\t")
        #
        #
        # dod = np.loadtxt(file)

    #     dod2 = pd.DataFrame(dod[:, 1:], index=dod[:, 0])
    #
    #
    #     _, delays = dod2.shape
    #     print("number of delays: ", delays)
    #
    #     test = (np.arange(0, delays - len(taxis), 1) + 1) * np.mean(np.diff(taxis)) + taxis[-1]
    #     print(test)
    #
    #     print("latest delay of original time axis: ", taxis[-1])
    #
    #
    #     #np.diff(taxis)
    #     print("mean delta t: ", np.mean(np.diff(taxis)))
    #
    #     t_axis_interp = np.append(taxis, test)
    #
    # print(files)


    #dod_test = pd.DataFrame(dod[:, 1:], index=dod[:, 0], columns=t_axis_interp)
    return dod #2, taxis, test, t_axis_interp, dod_test
