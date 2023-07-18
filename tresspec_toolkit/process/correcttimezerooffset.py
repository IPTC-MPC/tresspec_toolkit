
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy import interpolate



def correcttimezerooffset(data, t0=None):
    # function used to correct for wrong time zero by interpolation
    # t0
    if type(data) != list:
        data = [data]

    #     no_datasets = length(data);
    # else
    #     no_datasets = 1;
    #     data
    #     {1} = data;
    # end

    if type(t0) != list:
        t0 = [t0]
        #length(data) ~= length(time_offsets)
    #error('Mismatch between number of dataset and vector containing time offsets. Dimensions must agree. Abort!')
    #end

    for measurement in range(len(data)):
        print('t0....', t0[measurement])
        freq = data[measurement].index.to_numpy()
        tau = data[measurement].columns.to_numpy()
        # new_timeaxis = data[measurement].columns.to_numpy() - t0[measurement]

        old_timeaxis, old_freqaxis = np.meshgrid(tau, freq)
        new_timeaxis, new_freqaxis = np.meshgrid(tau - t0[measurement], freq)

        OLD = (old_timeaxis, old_freqaxis)
        NEW = (new_timeaxis, new_freqaxis)

        dod = data[measurement].values

        #Ti = interpolate.griddata((old_timeaxis, old_freqaxis),dod, (new_timeaxis, new_freqaxis), method='cubic')
        #print(Ti)

        #print(new_timeaxis, freq)

    return old_timeaxis, freq, dod, OLD, NEW
    #     dataset = 1:no_datasets
    # % % identifying
    # time
    # axis
    # if max(data{dataset}(:,
    # 1)) < 1050
    # time_axis_locations = 'dimension_1';
    # else
    # time_axis_locations = 'dimension_2';
    # data
    # {dataset} = transpose(data
    # {dataset});
    # end
    #
    # no_delays = size(data
    # {dataset}, 1) - 1;
    #
    # corrected_data
    # {dataset} = data
    # {dataset};

        #interpolate.griddata()



    #     for delay in data[measurement].columns:
    #         dod = data[measurement].loc[:, delay]
    #         treal = data{dataset}(1, 2: end);
    #         toffsetted = data{dataset}(1, 2: end) - time_offsets(dataset);
    #
    #         dod_inp = spline(toffsetted, dod, treal);
    #
    #         corrected_data{dataset}(delay + 1, 2: end) = dod_inp;
    #
    # Cubic - spline
    # >> >
    #
    # x = np.arange(0, 2 * np.pi + np.pi / 4, 2 * np.pi / 8)
    #
    # y = np.sin(x)
    #
    # tck = interpolate.splrep(x, y, s=0)
    #
    # xnew = np.arange(0, 2 * np.pi, np.pi / 50)
    #
    # ynew = interpolate.splev(xnew, tck, der=0)
    #
    # >> >
    #
    # plt.figure()
    #
    # plt.plot(x, y, 'x', xnew, ynew, xnew, np.sin(xnew), x, y, 'b')
    #
    # plt.legend(['Linear', 'Cubic Spline', 'True'])
    #
    # plt.axis([-0.05, 6.33, -1.05, 1.05])
    #
    # plt.title('Cubic-spline interpolation')
    #
    # plt.show()
    #
    # % transpose
    # back if required
    # if strcmp(time_axis_locations, 'dimension_2')
    #     corrected_data
    #     {dataset} = transpose(corrected_data
    #     {dataset});
    #     end
    #
    # end
    #
    # % make
    # data
    # an
    # array
    # again if necessary
    # if no_datasets == 1
    #     corrected_data = data
    #     {1};
    # end
    #
    # end