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


def stepscan(wrkpath, readparameters=False, temporalresolution=0, timestepsbeforezero=200):

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




    print("Classes working fine. Temporal resolution is ...", par.delta_t)
    print("Classes working fine. Tsbz is ...", par.timeslices_before_zero)
    print("and now and no longer empty attribute...", par.volume)
    print("and now and no longer empty attribute...", par.molecular_weight)

    data = np.loadtxt(wrkpath)

    wn, cols = data.shape

    # time slices, time slices before zero
    ts = cols - 1
    tsbz = 200

    # setting axes
    timeaxis = (np.arange(0, ts, 1) - (tsbz-1)) * temporalresolution
    wavenumbers = data[:, 0]

    intensity = pd.DataFrame(data[:, 1:], index=wavenumbers, columns=timeaxis)

    # extract data before laser pulse and average, compile into a matrix to facilitate computations
    intensity0 = intensity.iloc[:, intensity.columns < 0.0]
    intensity0mean = np.tile(intensity0.to_numpy().mean(axis=1).reshape(wn, 1), ts)

    # calculate dOD and parse into dataframe
    dod = 1000 * np.log10(intensity0mean / intensity)
    dod = pd.DataFrame(dod, index=wavenumbers, columns=timeaxis)


    #timeaxis = np.linspace(1, size(data{i}, 2), size(data
    #{i}, 2)) - t0) *Delta_t;

    #print('delays...', delays)
    return data, timeaxis, dod, par
#     def loadstepscandata(working_path):
#         data = np.loadtxt(working_path)
#         r, c = data.shape
#         #        print('# rows: ', r, '# columns: ', c)
#
#         no_runs = np.count_nonzero((data == data[0, :]).all(axis=1))
#         no_delays = int(r / no_runs - 1)
#         no_sb = np.count_nonzero(np.diff(data[0, 1:]) > 0) + 1
#         no_pixels = int((c - 1) / no_sb)
#
#         #           print('# runs: ', no_runs, '# delays: ', no_delays, '# stitching blocks:', no_sb, '# pixels: ', no_pixels)
#
#         scans = list()
#         for i in range(no_runs):
#             lower_index = i * no_delays + (i + 1)
#             upper_index = (i + 1) * no_delays + i
#
#             #            print('lower index: ', lower_index, 'data: ', data[lower_index, 0])
#             #            print('upper index: ', upper_index, 'data: ', data[upper_index, 0])
#
#             frequency_axis = 10 ** 7 / data[0, 1:]
#             delay_axis = data[lower_index:upper_index + 1, 0]
#
#             # scans[i] = pd.DataFrame(np.transpose(data[lower_index:upper_index + 1, 1:]),
#             #                         index=10 ** 7 / data[0, 1:],
#             #                         columns=data[lower_index:upper_index + 1, 0])
#
#
#             df = pd.DataFrame(np.transpose(data[lower_index:upper_index + 1, 1:]),
#                                     index=10 ** 7 / data[0, 1:],
#                                     columns=data[lower_index:upper_index + 1, 0])
#             scans.append(df)
#
#
#             scans[i] = scans[i].sort_index()
#         return scans
#
#     if os.path.isdir(wrkpath):
#         files = glob.glob(wrkpath + "/**/*_sve.dat", recursive=True)
#
#         counter = 0
#         tmp = list()
# #            tmp = []
#         for file in files:
#             #tmp[counter] = loaduvmirdata(file)
#             tmp.append(loadstepscandata(file))
#             counter += 1
#
#         counter = 0
#         runs = list()
#         #runs = []
#         for n in range(len(tmp)):
#             for m in range(len(tmp[n])):
#                 runs.append(tmp[n][m])
#                 #runs[counter] = tmp[n][m]
#                 counter += 1
#         return runs
#
#     elif os.path.isfile(wrkpath):
#         print('It is a file')
#         return loaduvmirdata(wrkpath)


# def loadUVMIRdata(path):
#
#     data = np.loadtxt(path)
#     r, c = data.shape
#     print('# rows: ', r, '# columns: ', c)
#
#     #if tom == 'UVMIR':
#     #elif tom == 'step-scan':
#
#     #data2 = np.transpose(data)
#
#     # rip apart into measurements
#     # sort
#     # convert to frequency domain
#
#     # function[DATA, no_runs, no_stitching_blocks, no_delays, no_pixels] = extract_runs_and_stitching_blocks(data)
#
#     #[DATA, no_runs, no_stitching_blocks, no_delays, no_pixels] = extract_runs_and_stitching_blocks(data)
#
#     # extract_runs_and_stitching_blocks is used to seperate the output into the different runs and stitching blocks
#     #
#     # Type extract_runs_and_stitching_blocks(data) with
#     #    - "data" being the matrix storing the dataset in usual format
#     #           - x along data(:, 1)
#     #           - y along data(1,:)
#     #           - z in data(2: end, 2: end)
#     # to return the data set separated into the different runs and stitching blocks
#     # ("DATA"(having the same format as "data")), the number of runs and stitching blocks applied for this measurement,
#     # and the number of delays for which data points were collected.
#
#
# #     [r, c] = size(data);
# #
# #     % determine
# #     number
# #     of
# #     runs, delays, stitching
# #     blocks and pixels
# #     no_runs = nnz(ismember(data, data(1,:), 'rows'));
# #     no_delays = r / no_runs - 1;
# #     no_stitching_blocks = length(find(diff(data(1, 2:end)) > 0))+1;
# #     no_pixels = (c - 1) / no_stitching_blocks;
# #
# #     % extract
# #     number
# #     of
# #     stitching
# #     blocks
# #     % no_stitching_blocks = 1;
# #     % for i = 2:c - 1
# #     % if (data(1, i) - data(1, i + 1) < 0)
# #
# # % no_stitching_blocks = no_stitching_blocks + 1;
# # % end
# # % end
# #
# # % number
# # of
# # pixels
# # per
# # stitching
# # run
# # % pixels = (c - 1) / no_stitching_blocks;
# #
# # % extract
# # number
# # of
# # delays
# # % delays = 0;
# # % for i = 2:r
# #
# # % if data(i, 2: end) ~ = data(1, 2:end)
# # % delays = delays + 1;
# # % else
# # % break
# # % end
# # % end
# #
# # % no_runs = (r / (delays + 1));
# #
# # % extract
# # stitching
# # blocks
# # per
# # run and store
# # them
# # separately in cell
# # variable
# # for j = 1:no_runs
# # for k = 1:no_stitching_blocks
# # DATA
# # {j, k} = [data((j - 1) * no_delays + j:j * (no_delays + 1), 1), ...
# # data((j - 1) * no_delays + j: j * (no_delays + 1), (k - 1) * no_pixels + 2: k * no_pixels + 1)];
# # end
# # end
# # end
# #
# #
# #
# #
# #     data2[data2[:, 0].argsort()]
#
# #    wn = 10**7 / data2[1:, 0]
#     return data
#
#
# def addnum(a, b):
#     return a+b
