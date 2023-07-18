# brought to you by J. Schmidt

import numpy as np
import scipy.stats as spstats
import scipy as sp
import re
import matplotlib.pyplot as plt
import matplotlib as mpl
import os
import glob
from mpl_toolkits.axes_grid1 import make_axes_locatable


# UV-mIR
def wavelengthextraction(filename):
    # extraction of the wavelength axis
    wavelength = filename[0].split()  # reading wavelength axis
    wavelength = wavelength[1:]  # cut off the first 0
    i = 0
    for wn in wavelength:
        wavelength[i] = float(wn)  # convert string into float
        i += 1
    return (wavelength)


def dataextraction(filename):
    idx = 0
    OD = []  # save of the raw OD data
    delays = []  # save of the delay times
    ODtemp = []  # temporary save of one OD block
    timetemp = []  # temporary save of one delay block
    blockidx = []  # list with the starting index of each block
    i = False
    for line in filename:
        if i == False:  # ignore wavelength axis
            i = True  # begin the readin of the next block in the next line
            blockidx.append(idx)  # safe the starting index of the block
        else:
            if len(line) != 1:  # check if line is blank
                line = line[:].split()
                ODtemp.append(line[1:])  # accumulate OD block
                timetemp.append(line[0])  # accumulate the delay times
                idx += 1  # count the lines of the block
            else:
                i = False  # blank line --> next line will be a wavelength line
                OD.extend(ODtemp)  # save OD block
                delays = timetemp  # safe delay block
                ODtemp = []  # ready temp OD block
                timetemp = []  # ready temp delay block
    return (OD, delays, blockidx)


def inputaverageddata(filename):
    file = open(filename).readlines()
    dat = file[0].split()
    freq = np.array(dat[1:]).astype(float)

    tmp = np.genfromtxt(filename, skip_header=1)
    delays = tmp[:, 0].copy()
    data = tmp[:, 1:].copy()

    return (data, freq, delays)

def inputglotaranfile(path):
    tmp = np.genfromtxt(path, skip_header=4)
    freq = tmp[0, :].copy()
    delays = tmp[1:, 0].copy()
    data = tmp[1:, 1:].copy()
    return (data, freq, delays)


def getidx(value, data):
    idx = (np.abs(np.array(data) - value)).argmin()
    return (idx)


def basedataextraction(filename):
    OD = []
    i = False
    for line in filename:
        if i == False:  # ignore freq axis
            i = True  # begin the readin of the next block in the next line
        else:
            if len(line) != 1:  # check if line is blank
                line = line[:].split()
                OD.append(line[1:])  # accumulate OD block
    return (OD)


def stitching(OD, wavelength):
    blocklength = int(len(wavelength) / 4)
    OD = np.array(OD).astype(float)
    ODstitch = []

    for line in OD:
        reg1 = line[:blocklength]
        reg2 = line[blocklength:2 * blocklength]
        reg3 = line[2 * blocklength:3 * blocklength]
        reg4 = line[3 * blocklength:4 * blocklength]
        ref1 = sp.interpolate.interp1d(wavelength[:blocklength],
                                       reg1)  # interpolate over a stitching block, done for all 4 seperatly
        ref2 = sp.interpolate.interp1d(wavelength[blocklength:2 * blocklength], reg2)
        ref3 = sp.interpolate.interp1d(wavelength[2 * blocklength:3 * blocklength], reg3)
        ref4 = sp.interpolate.interp1d(wavelength[3 * blocklength:4 * blocklength], reg4)

        corrfac1 = sum(
            # calculation of a correction factor for each stitching block by comparing a point to the average of the point to the four intrpolations, done for all points of a time step
            ((reg1[1:-1] - ref1(wavelength[1:blocklength - 1])) + (reg1[1:-1] - ref2(wavelength[1:blocklength - 1])) + \
             (reg1[1:-1] - ref3(wavelength[1:blocklength - 1])) + (
                     reg1[1:-1] - ref4(wavelength[1:blocklength - 1]))) / 4) / len(reg1[1:-1])
        corrfac2 = sum(((reg2[1:-1] - ref1(wavelength[blocklength + 1:2 * blocklength - 1])) + (
                reg2[1:-1] - ref2(wavelength[blocklength + 1:2 * blocklength - 1])) + \
                        (reg2[1:-1] - ref3(wavelength[blocklength + 1:2 * blocklength - 1])) + (
                                reg2[1:-1] - ref4(wavelength[blocklength + 1:2 * blocklength - 1]))) / 4) / len(
            reg2[1:-1])
        corrfac3 = sum(((reg3[1:-1] - ref1(wavelength[2 * blocklength + 1:3 * blocklength - 1])) + (
                reg3[1:-1] - ref2(wavelength[2 * blocklength + 1:3 * blocklength - 1])) + \
                        (reg3[1:-1] - ref3(wavelength[2 * blocklength + 1:3 * blocklength - 1])) + (
                                reg3[1:-1] - ref4(wavelength[2 * blocklength + 1:3 * blocklength - 1]))) / 4) / len(
            reg3[1:-1])
        corrfac4 = sum(((reg4[1:-1] - ref1(wavelength[3 * blocklength + 1:4 * blocklength - 1])) + (
                reg4[1:-1] - ref2(wavelength[3 * blocklength + 1:4 * blocklength - 1])) + \
                        (reg4[1:-1] - ref3(wavelength[3 * blocklength + 1:4 * blocklength - 1])) + (
                                reg4[1:-1] - ref4(wavelength[3 * blocklength + 1:4 * blocklength - 1]))) / 4) / len(
            reg4[1:-1])
        corrreg1 = reg1 - corrfac1
        corrreg2 = reg2 - corrfac2
        corrreg3 = reg3 - corrfac3
        corrreg4 = reg4 - corrfac4
        reg = np.concatenate((corrreg1, corrreg2, corrreg3, corrreg4), axis=None)
        ODstitch.append(reg)
    ODstitch = np.array(ODstitch).astype(float)
    return (ODstitch)


def convert(wavelength):
    return ([10000000 / x for x in wavelength])  # convert wavelength into frequency axis


def sort(freq, data):
    freqsort = sorted(freq)  # sort the frequency axis

    reorder = []
    for x in freqsort:
        reorder.append(freq.index(x))  # build a reorder index file by comparing unordered
        # and ordered frequency axis
    orddata = []
    orddata[:] = data[:, reorder]  # order the data according to the reordering index file
    return (freqsort, orddata)


def linearbaselinecorr(xaxis, data, baseline):
    i = 0
    for line in data:  # loop over all timesteps
        factor = 1
        region = []
        x_regress = []
        y_regress = []

        for wn in baseline:  # extract the indices of the border frequencies
            idx = (np.abs(np.array(xaxis) - wn)).argmin()

            region.append(int(idx))

        while len(region) >= 1:  # fill matrices with freq and OD data
            x1 = region.pop()
            x2 = region.pop()
            x_regress.extend(xaxis[x2:x1])
            y_regress.extend(line[x2:x1])

        slope, intercept, r_value, p_value, std_err = spstats.linregress(x_regress,
                                                                         y_regress)  # calculate a linear regression

        data[i] = line - factor * (slope * np.array(xaxis) + intercept)  # subtract baseline from data
        i += 1
    return data


def staticbaselinecorr(data, baseline, xaxis):
    v = []
    region = []
    i = 0
    for wn in baseline:  # extract the indices of the border frequencies
        idx = (np.abs(np.array(xaxis) - wn)).argmin()
        region.append(int(idx))

    for line in data[:]:  # mean of the data given by the baseline for each delay
        av = (np.sum(line[region[0]:region[1]])) / (float(region[1]) - float(region[0]))
        data[i] = line - av  # subtract the mean of each delay from the data at this delay
        i += 1
    return (data)


def comparativebaselinecorrection(data, freq, basedataname, blockidx):
    basedatas = open(basedataname).readlines()
    basefreq = wavelengthextraction(basedatas)
    basedata = basedataextraction(basedatas)
    basedatas.close()
    basedata = np.array(basedata).astype(float)
    data = np.array(data).astype(float)
    OD = []

    i = 0
    for line in data:
        if i == blockidx[1]:
            i = 0
        basedataref = sp.interpolate.interp1d(basefreq, basedata[i, :])
        corrfac = sum(line[1:-1] - basedataref(freq[1:-1])) / len(line[1:-1])
        reg = line - corrfac
        OD.append(reg)
        i += 1

    return (OD)


def artifact(xaxis, data, timestop, Grad):
    av = np.nanmean(data[:,:timestop], axis=1)
    poly = np.poly1d(np.polyfit(xaxis, av, Grad))
    baseline = poly(xaxis)
    i = 0
    for line in data[:]:  # subtract the artifact from all timesteps
        data[i] = (line - baseline)
        i += 1
    plt.plot(xaxis, av, 'blue', xaxis, baseline, 'purple')  # , xnew, avdense, 'red')
    plt.show()
    return (data)


def meanartifact(data, t1, t2, time):
    timelow = getidx(t1, time)
    timehigh = getidx(t2, time)
    artifact = np.mean(data[timelow:timehigh, :], axis=0)
    data -= artifact
    return (data)


def Sumsspectra(OD, time, steps, timestart):
    ODtemp = np.zeros((len(OD[0])))  # prepare an array
    cutOD = OD[-timestart + 1:, :]
    cuttime = time[-timestart + 1:]
    newtime = []
    newOD = []
    i = 0
    j = 0
    for line in cutOD:
        if i < (steps - 1):  # sum over all ODs in one window
            ODtemp += line
            i += 1
        elif (j + 1) * (i + 1) > len(cuttime):  # if a timestep larger than the measured timestep is called, break
            break
        elif i == (steps - 1):  # save the window average of the current finished window and begin a new window
            ODtemp += line
            newOD.append(ODtemp)
            newtime.append(cuttime[(j + 1) * (i + 1) - 1])
            i = 0
            j += 1
            ODtemp = np.zeros((len(OD[0])))
    newOD = np.array(newOD).astype(float) / steps
    newtime = np.array(newtime).astype(float)
    return (newOD, newtime)


def takeaverage(OD, blockidx):
    ODav = OD[0]
    ODav = np.array(ODav).astype(float)
    ODav -= ODav
    OD = np.array(OD).astype(float)
    i = 0
    for line in blockidx[0:-1]:
        i += 1
        ODav = ODav + OD[line:(blockidx[i])]  # average the different OD blocks into one
    ODav = ODav + OD[blockidx[-1]:(blockidx[-1] + blockidx[1])]
    ODav /= float(len(blockidx))
    return (ODav)


def wavelengthshiftdetermination(data, freq, Averageoflastspectra, statOD):
    Av = np.zeros(len(data[1]))
    i = Averageoflastspectra

    for line in data:
        while i > 0:
            Av += data[-i]
            i -= 1
    Av /= Averageoflastspectra
    plt.plot(freq, Av, 'ko', freq, statOD, 'ro')
    plt.title('wavelenghtshift determination at Av of last delays')
    plt.show()


def linearwavelengthshift(data, wavelength, Averageoflastspectra, statspectraname):
    # shifts the data on the wavelength axis according to a linear equation referenced to a stationay spectrum
    # has to be given wavelengths!
    # has to have a 'coords = []' in the global environment to work
    freq = convert(wavelength)
    statOD = statspectrainput(freq, statspectraname, -3, 0)

    Av = np.zeros(len(data[1]))
    i = Averageoflastspectra
    for line in data:
        while i > 0:
            Av += data[-i]
            i -= 1
    Av /= Averageoflastspectra

    print('First pick two signals in the data set, starting with the lower wavenumber. Then pick the correspondent '
          'signals in the stationary spectrum')
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(wavelength, Av, 'ko', label='unshifted data')
    ax.plot(wavelength, statOD, 'ro', label='stationary spectrum')


    points = fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show()
    fig.canvas.mpl_disconnect(points)
    global coords
    points = coords

    m = (points[1] - points[0]) / (points[3] - points[2])
    b = points[0]-m*points[2]
    shiftedwavelength = np.zeros(len(wavelength))
    for index, element in enumerate(np.array(wavelength).astype(float)):
        shiftedwavelength[index] = (element / m) - (b / m)


    plt.plot(wavelength, Av, 'ko', label='unshifted data')
    plt.plot(wavelength, statOD, 'ro', label='stationary spectrum')
    plt.plot(shiftedwavelength, Av, 'go', label='shifted data')
    plt.legend()
    plt.show()
    return(shiftedwavelength)


def onclick(event):
    # returns coords with the x coordinates of the positions clicked in the plot
    # has to have a 'coords = []' in the global environment to work
    ix = event.xdata
    print('x = ', ix)
    global coords
    coords.append(ix)


def statspectrainput(freq, statname, statscale, statbaseoffset):
    statOD = []
    statfreq = []

    fh = open(statname + '.txt').readlines()
    i = 0
    for line in fh:  # readin of stationary spectra OD and freq axis
        line = line.split()
        statfreq.append(float(line[0]))
        statOD.append(float(line[1]))

    low = getidx(freq[0] - 10.0, statfreq)  # find the necessary freq region
    high = getidx(freq[-1] + 10.0, statfreq)

    statfreq = statfreq[low:high]  # truncate the stationary spectrum
    statOD = statOD[low:high]  # to the measured freq region
    i = 0
    for line in statOD:  # shift and scale the stat spectra
        statOD[i] = (line * statscale) - statbaseoffset
        i += 1

    int = sp.interpolate.interp1d(statfreq, statOD)  # interpolate stat spectra to measured
    interpstatOD = int(freq)  # freq axis

    file8 = open('scaledstatspectra.dat', 'w')
    i = 0
    for line in freq:
        file8.write(str(line) + ' ' + str(interpstatOD[i]) + '\n')
        i += 1
    file8.close()
    return interpstatOD, statfreq, statOD


def importstatspectra(statname):
    statOD = []
    statfreq = []

    fh = open(statname + '.txt').readlines()
    i = 0
    for line in fh:  # readin of stationary spectra OD and freq axis
        line = line.split()
        statfreq.append(float(line[0]))
        statOD.append(float(line[1]))
    statfreq = np.array(statfreq).astype(float)
    statOD = np.array(statOD).astype(float)
    return statfreq, statOD


def productspectracalc(statname, statscale, statbaseoffset, OD, freq):
    interpstatOD, statfreq, statOD = statspectrainput(freq, statname, statscale, statbaseoffset)
    i = 0
    prodOD = np.empty_like(OD)
    for line in OD:  # calculate product spectra
        prodOD[i] = line - interpstatOD
        i += 1
    plt.plot(freq, interpstatOD, 'red', freq, OD[100], 'black', freq, prodOD[100], 'blue')
    plt.title('productspectra')
    plt.show()
    return (prodOD)


def root(prodOD, delays, freqsort, polyorder, polyregion):
    roots = np.empty([len(delays), polyorder - 1])

    region = []
    for wn in polyregion:
        idx = (np.abs(np.array(freqsort) - wn)).argmin()
        region.append(int(idx))

    i = 0
    for line in prodOD:
        roots[i] = np.roots(np.polyder(np.polyfit(freqsort[region[0]:region[1]], line[region[0]:region[1]], polyorder)))
        i += 1

    name = 'roots.dat'
    file = open(name, 'w')
    i = 0
    for line in delays[:]:
        file.write(str(line) + ' ' + " ".join([str(element) for element in roots[i]]) + '\n')
        i += 1
    file.close()


def followmaxima(freq, delays, OD, region, name):
    maxfreq = []
    maxOD = []
    low = getidx(region[0], freq)
    high = getidx(region[1], freq)
    ODcut = OD[:, low:high]
    freqcut = freq[low:high]
    for line in ODcut:
        maxOD.append(np.max(line))
        maxfreq.append(freqcut[getidx(maxOD[-1], line)])
    maxfreq = np.array(maxfreq)
    maxOD = np.array(maxOD)

    title = name + '_followmaxima' + str(region[0]) + '-' + str(region[1]) + '.ascii'
    file = open(title, 'w')
    i = 0
    for line in delays[:]:
        file.write(str(line) + ' ' + str(maxfreq[i]) + ' ' + str(maxOD[i]) + '\n')
        i += 1
    file.close()

def merge2datasetsandsort(data1, freq1, data2, freq2):
    # merging of data
    OD = np.concatenate((data1, data2), axis=1)
    wn = np.append(freq1, freq2)

    # sorting of data with freq axis
    wnsort, ODsort = sort(np.ndarray.tolist(wn), OD)
    ODsort = np.array(ODsort).astype(float)
    wnsort = np.array(wnsort).astype(float)
    return (ODsort, wnsort)


def averagingoftooclosedatapoints(ODsort, wnsort, threshold):
    # generating a list of indexes of all freq points which are closer than threshold together
    index = []
    for idx, line in enumerate(wnsort):
        if idx == len(wnsort) - 2:
            break
        if wnsort[idx + 1] - line <= threshold:
            index.append(idx)

    # determination of the number of odd and even indices, only keep odd indices in the index when
    # the most are odd or vise versa to avoid averaging one point two times
    even = 0
    odd = 0
    for num in index:
        if num % 2 == 0:
            even += 1
        else:
            odd += 1
    if even >= odd:
        for num in index:
            if num % 2 != 0:
                index.remove(num)
    if odd >= even:
        for num in index:
            if num % 2 == 0:
                index.remove(num)

    # averaging of too close data points with the updated list of indices:
    freqav = []
    ODav = []
    for idx, num in enumerate(wnsort):
        if idx - 1 in index:
            pass
        elif idx in index:
            freqav.append((num + wnsort[idx + 1]) / 2)
            ODav.append((ODsort[:, idx] + ODsort[:, idx + 1]) / 2)
            pass
        else:
            freqav.append(num)
            ODav.append(ODsort[:, idx])
    freqav = np.array(freqav).astype(float)
    ODav = np.transpose(np.array(ODav).astype(float))
    return (ODav, freqav)


def averagelasttimesteps(data, numberoftimesteps):
    i = numberoftimesteps
    Av = np.zeros(len(data[0]))
    for line in data:
        while i > 0:
            Av += data[-i]
            i -= 1
    Av /= numberoftimesteps
    return (Av)

def fmt(x, pos):
  a, b = '{:.1e}'.format(x).split('e')
  b = int(b)
  return r'${}$'.format(a, b)

def shiftedColorMap(cmap, start=0, midpoint=0.5, stop=1.0, name='shiftedcmap'):
    '''
    Function to offset the "center" of a colormap. Useful for
    data with a negative min and positive max and you want the
    middle of the colormap's dynamic range to be at zero.

    Input
    -----
      cmap : The matplotlib colormap to be altered
      start : Offset from lowest point in the colormap's range.
          Defaults to 0.0 (no lower offset). Should be between
          0.0 and `midpoint`.
      midpoint : The new center of the colormap. Defaults to
          0.5 (no shift). Should be between 0.0 and 1.0. In
          general, this should be  1 - vmax / (vmax + abs(vmin))
          For example if your data range from -15.0 to +5.0 and
          you want the center of the colormap at 0.0, `midpoint`
          should be set to  1 - 5/(5 + 15)) or 0.75
      stop : Offset from highest point in the colormap's range.
          Defaults to 1.0 (no upper offset). Should be between
          `midpoint` and 1.0.
    '''
    cdict = {
        'red': [],
        'green': [],
        'blue': [],
        'alpha': []
    }

    # regular index to compute the colors
    reg_index = np.linspace(start, stop, 257)

    # shifted index to match the data
    shift_index = np.hstack([
        np.linspace(0.0, midpoint, 128, endpoint=False),
        np.linspace(midpoint, 1.0, 129, endpoint=True)
    ])

    for ri, si in zip(reg_index, shift_index):
        r, g, b, a = cmap(ri)

        cdict['red'].append((si, r, r))
        cdict['green'].append((si, g, g))
        cdict['blue'].append((si, b, b))
        cdict['alpha'].append((si, a, a))

    newcmap = mpl.colors.LinearSegmentedColormap(name, cdict)
    plt.register_cmap(cmap=newcmap)

    return newcmap

def plotting(ODav, freqsort, delays):
    plt.figure(figsize=(10, 20))
    shiftedcmap = shiftedColorMap(mpl.cm.seismic, midpoint=(1-np.amax(ODav)/(np.amax(ODav)+np.abs(np.amin(ODav)))))


    cp = plt.contourf(freqsort, delays, ODav, locator=mpl.ticker.MaxNLocator(200), origin='lower', cmap=shiftedcmap)
    ax = plt.gca()
    ax.set_xlim(round(freqsort[0], -1), round(freqsort[-1], -1))
    ax.set_ylim(0.1, delays[-1])
    ax.spines['bottom'].set_visible(False)
    ax.tick_params(which='major', bottom=False, top=True, right=True, width=1, length=4, labelbottom=False, labelsize=16)
    ax.tick_params(which='both', direction='in')
    ax.set_yscale('log')
    plt.ylabel('delay / ps', fontsize=16)

    cbar = plt.colorbar(cp, format=mpl.ticker.FuncFormatter(fmt), location='right')
    cbar.ax.set_ylabel('\u0394mOD', fontsize=16)
    cbar.ax.tick_params(labelsize=16)

    divider = make_axes_locatable(ax)
    axlin = divider.append_axes("bottom", size=1.0, pad=0.01, sharex=ax)
    cs = axlin.contourf(freqsort, delays, ODav, locator=mpl.ticker.MaxNLocator(200),
          origin='lower', cmap=shiftedcmap)
    axlin.set_xlim(round(freqsort[0], -1), round(freqsort[-1], -1))
    axlin.set_ylim(-250, 0)
    axlin.spines['top'].set_visible(False)
    axlin.tick_params(which='both', direction='in', bottom=True,  top=False, right=True, width=1, length=4, labelbottom=True, labelsize=16)
    axlin.set_yscale('linear')
    axlin.set_yticks((-200, -100))
    plt.xlabel('$\mathit{\u1E7D}$ / $\mathregular{cm^{-1}}$', fontsize=16)

    plt.show()

def plottingmesh(ODav, freqsort, delays):
    plt.figure(figsize=(10, 20))
    shiftedcmap = shiftedColorMap(mpl.cm.seismic,midpoint=(1 - np.amax(ODav) / (np.amax(ODav) + np.abs(np.amin(ODav)))))
    cp = plt.pcolormesh(freqsort, delays, ODav, cmap=shiftedcmap)
    ax = plt.gca()
    ax.set_xlim(round(freqsort[0], -1), round(freqsort[-1], -1))
    ax.set_ylim(0.1, delays[-1])
    ax.spines['bottom'].set_visible(False)
    ax.tick_params(which='major', bottom=False, top=True, right=True, width=1, length=4, labelbottom=False,
                   labelsize=16)
    ax.tick_params(which='both', direction='in')
    ax.set_yscale('log')
    plt.ylabel('delay / ps', fontsize=16)
    cbar = plt.colorbar(cp, format=mpl.ticker.FuncFormatter(fmt), location='right')
    cbar.ax.set_ylabel('\u0394mOD', fontsize=16)
    cbar.ax.tick_params(labelsize=16)
    divider = make_axes_locatable(ax)
    axlin = divider.append_axes("bottom", size=1.0, pad=0.01, sharex=ax)
    cs = axlin.pcolormesh(freqsort, delays, ODav, cmap=shiftedcmap)
    axlin.set_xlim(round(freqsort[0], -1), round(freqsort[-1], -1))
    axlin.set_ylim(-250, 0)
    axlin.spines['top'].set_visible(False)
    axlin.tick_params(which='both', direction='in', bottom=True, top=False, right=True, width=1, length=4,
                      labelbottom=True, labelsize=16)
    axlin.set_yscale('linear')
    axlin.set_yticks((-200, -100))
    plt.xlabel('$\mathit{\u1E7D}$ / $\mathregular{cm^{-1}}$', fontsize=16)
    plt.show()

def plottransientlog(data, freq, delays, Transient):
    dat = np.transpose(data)

    fig = plt.figure(figsize=(20, 10))
    grid = plt.GridSpec(1,1)

    ax = fig.add_subplot(grid[0, 0])
    ax.spines['right'].set_visible(False)
    ax.set_xscale('linear')
    ax.tick_params(direction='in', top=True, right=False, left=True, width=1, length=4, labelbottom=True, labelsize=16)
    ax.set_ylabel('\u0394mOD', fontsize=16)

    divider = make_axes_locatable(ax)
    axlin = divider.append_axes("right", size=13, pad=0.01, sharey=ax)
    axlin.spines['left'].set_visible(False)
    axlin.tick_params(direction='in', top=True, right=True, left=False, width=1, length=4, labelleft=False, labelright=True, labelbottom=True, labelsize=16)
    axlin.set_xscale('log')
    axlin.set_xlabel('delay / ps', fontsize=16)

    for line in Transient:
        position = getidx(line, freq)
        ax.plot(delays[:getidx(0.1, delays)], dat[position, :getidx(0.1, delays)], label='Transient ' + str(round(freq[position], 1)) + ' $\mathregular{cm^{-1}}$')
        axlin.plot(delays[getidx(0.1, delays):], dat[position, getidx(0.1, delays):], label='Transient ' + str(round(freq[position], 1)) + ' $\mathregular{cm^{-1}}$')

    plt.legend()
    plt.show()



def plottransient(data, freq, delays, Transient):
    position = getidx(Transient, freq)
    dat = np.transpose(data)

    plt.plot(delays, dat[position], label='Transient ' + str(round(freq[position], 1)) + ' $\mathregular{cm^{-1}}$')
    ax = plt.gca()
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    #ax.set_xscale('log')
    ax.tick_params(direction='in', top=True, right=True, width=1, length=4, labelbottom=True)
    plt.xlabel('delay / ps', fontsize=16)
    plt.ylabel('\u0394mOD', fontsize=16)


def plotTransSpec(data, freq, delays, TransSpec):
    position = getidx(TransSpec, delays)

    plt.plot(freq, data[position], label=str(round(delays[position], 1)) + ' ps')
    ax = plt.gca()
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    #ax.set_xscale('log')
    ax.tick_params(direction='in', top=True, right=True, width=1, length=4, labelbottom=True)
    plt.xlabel('wavenumber / $\mathregular{cm^{-1}}$', fontsize=16)
    plt.ylabel('\u0394mOD', fontsize=16)


def plot2transients(data, freq, delays, label, data2, freq2, delays2, label2, Transient):
    position = getidx(Transient, freq)
    data = np.transpose(data)
    position2 = getidx(Transient, freq2)
    data2 = np.transpose(data2)

    plt.figure()
    plt.plot(delays, data[position], label=label)
    plt.plot(delays2, data2[position2], label=label2)
    plt.title('Transient ' + str(round(freq[position], 1)) + ' $\mathregular{cm^{-1}}$')
    ax = plt.gca()
    #plt.xticks(np.arange(0, delays[-1] + 10, 250), fontsize=16)
    plt.yticks(fontsize=16)
    #ax.set_xscale('log')
    ax.tick_params(direction='in', top=True, right=True, width=1, length=4, labelbottom=True)
    plt.xlabel('delay / ps', fontsize=16)
    plt.ylabel('\u0394mOD', fontsize=16)
    plt.show()


def plot3transientspectraagainststat(name, time, delay, freq1, dat1, freq2, dat2, freq3, dat3, statfreq, statdat):
    idx = getidx(time, delay)
    plt.plot(freq1, dat1[idx, :], 'black', freq2, dat2[idx, :], 'blue', freq3, dat3[idx, :], 'red',
                statfreq, statdat, 'green')
    plt.title(str(name) + ' ' + str(time))
    plt.show()


def plotMeanTransientbetween(data, freq, delay, range):
    low = getidx(range[0], freq)
    high = getidx(range[1], freq)
    Transient = np.nanmean(data[:, low:high], axis=1)

    plt.figure()
    plt.plot(delay, Transient)
    plt.title('Transient between ' + str(round(freq[low], 1)) + ' $\mathregular{cm^{-1}}$ and ' + str(
        round(freq[high], 1)) + ' $\mathregular{cm^{-1}}$, ' + str(high-low) + ' datapoints')
    ax = plt.gca()
    plt.xticks(np.arange(delay[0], delay[-1] + 10, 100), fontsize=16)
    plt.yticks(fontsize=16)
    ax.set_xscale('log')
    ax.tick_params(direction='in', top=True, right=True, width=1, length=4, labelbottom=True)
    plt.xlabel('delay / ps', fontsize=16)
    plt.ylabel('\u0394mOD', fontsize=16)
    plt.show()



def outputmajorTransients(data, time, freq, Transient):
    # major transients
    majortransient = np.empty((len(time), len(Transient)))
    for i, line in enumerate(Transient):
        majortransient[:, i] = data[:, getidx(line, freq)]
    output('MajorTransientsforLuis', Transient, time, majortransient)


def output(title, xaxis, yaxis, data):
    name = title + '.dat'
    file = open(name, 'w')
    file.write(str(0) + ' ')
    file.write(" ".join([str(element) for element in xaxis]) + '\n')
    i = 0
    for line in yaxis[:]:
        file.write(str(line) + ' ' + " ".join([str(element) for element in data[i]]) + '\n')
        i += 1
    file.close()
