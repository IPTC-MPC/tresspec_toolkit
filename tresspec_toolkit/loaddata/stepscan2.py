import numpy as np
import pandas as pd
import os
import glob


class Parameters:
    def __init__(self, delta_t, timeslices_before_zero):
        self.delta_t = delta_t
        self.timeslices_before_zero = timeslices_before_zero
        self.timeslices = ""
        self.compound = ""
        self.quencher = ""
        self.solvent = ""
        self.mass = ""
        self.molecular_weight = ""
        self.volume = ""
        self.d = ""
        self.lambda_exc = ""
        self.E_exc = ""

    def setparameter(self, string, value):
        if string == "timeslices":
            self.timeslices = value
        elif string == "compound":
            self.compound = value
        elif string == "quencher":
            self.quencher = value
        elif string == "solvent":
            self.solvent = value
        elif string == "mass":
            self.mass = value
        elif string == "molecular_weight":
            self.molecular_weight = value
        elif string == "volume":
            self.volume =value
        elif string == "d":
            self.d = value
        elif string == "lambda_exc":
            self.lambda_exc =value
        elif string == "E_exc":
            self.E_exc =value


def stepscan2(wrkpath, readparameters=False, temporalresolution=0, timestepsbeforezero=200):


    par = Parameters(temporalresolution, timestepsbeforezero)
    print("Classes working fine. Temporal resolution is ...", par.delta_t)
    print("Classes working fine. Tsbz is ...", par.timeslices_before_zero)
    print("and now and empty attribute...", par.volume)

    def loadparameters(parpth, parclass):
        parfile = open(parpth)
        lines = parfile.readlines()

        for line in lines:
            flag = line.split()[0]
            value = line.split()[-1]
            print(line.split()[0], "is attribute of class: ", hasattr(parclass, line.split()[0]))
            print("value of parameter", line.split()[-1])
            parclass.setparameter(flag, value)

        parfile.close()
        return parclass

    if readparameters:
        pth = os.path.dirname(os.path.dirname(wrkpath))
        files = glob.glob(pth + "/**/parameters.txt", recursive=True)
        if bool(files):
            print("Parameters file found. Loading parameters from ...\n", files)
            loadparameters(files[0], par)
        else:
            print("No parameters file found. Please specify explicitly")




    def load_step_scan_spectrum(pth_file, no_delays_before_zero):
        # loading data
        data = np.loadtxt(pth_file)

        _, cols = data.shape

        no_delays = cols - 1

        # calculating time axis and extracting frequency axis
        time_axis = (np.arange(0, no_delays, 1) - (no_delays_before_zero - 1)) * temporalresolution
        frequencies = data[:, 0]

        dod = pd.DataFrame(1000 * data[:, 1:], index=frequencies, columns=time_axis)
        return dod



    #intensity = pd.DataFrame(data[:, 1:], index=wavenumbers, columns=time_axis)

    # extract data before laser pulse and average, compile into a matrix to facilitate computations
    #intensity0 = intensity.iloc[:, intensity.columns < 0.0]
    #intensity0mean = np.tile(intensity0.to_numpy().mean(axis=1).reshape(wn, 1), ts)

    # calculate dOD and parse into dataframe
    #dod = 1000 * np.log10(intensity0mean / intensity)
    #dod = pd.DataFrame(dod, index=wavenumbers, columns=time_axis)


    #dod = pd.DataFrame(data[:, 1:], index=data[:, 0], columns=time_axis)

    #time_axis = np.linspace(1, size(data{i}, 2), size(data
    #{i}, 2)) - t0) *Delta_t;

    #print('delays...', delays)



    #########################################################################
    #                                                                       #
    #    final code to load the data, either from directory or from file    #
    #                                                                       #
    #########################################################################
    if os.path.isdir(wrkpath):
        runs = list()
        files = glob.glob(wrkpath + "/**/*DC.0.dpt", recursive=True)



        # initialization
        # counter = 0
        # tmp = list()
        # tmp_sb = list()
        #
        for file in files:
            runs.append(load_step_scan_spectrum(file, timestepsbeforezero))
        #     tmp.append(runs_tmp)
        #     tmp_sb.append(runs_sb_tmp)
        #     counter += 1
        #
        # runs = list()
        # runs_sb = list()
        #
        # for n in range(len(tmp)):
        #     for m in range(len(tmp[n])):
        #         runs.append(tmp[n][m])
        #         runs_sb.append(tmp_sb[n][m])
        #
        # return runs, runs_sb
        #runs = files

    elif os.path.isfile(wrkpath):
        print("came here")
        runs = load_step_scan_spectrum(wrkpath, timestepsbeforezero)

    return runs
