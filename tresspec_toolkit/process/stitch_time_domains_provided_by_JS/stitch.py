# brought to you by J. Schmidt

import numpy as np
import matplotlib.pyplot as plt
from subroutines import output, plotting, plottransientlog, plotTransSpec, convert, getidx, statspectrainput, plottingmesh
from scipy import signal, interpolate


def linearwavelengthshift(data, wavelength, delays, statspectraname, timetowatch):
    """ shifts the data on the wavelength axis according to a linear equation referenced to a stationary spectrum
    has to be given wavelengths!
    has to have a 'coords = []' in the global environment to work"""
    freq = convert(wavelength)
    interpstatOD, statfreq, statOD = statspectrainput(freq, statspectraname, -1, 0)

    Early = data[getidx(timetowatch, delays), :]
    scale = np.amax(np.abs(Early))/np.amax(np.abs(statOD))
    statOD = np.array(statOD)*scale

    print('First pick two signals in the data set, starting with the lower wavenumber. Then pick the corresponding '
          'signals in the stationary spectrum')
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(wavelength, Early, 'ko-', label='unshifted data')
    ax.plot(convert(statfreq), statOD, 'r-', label='stationary spectrum')

    points = fig.canvas.mpl_connect('button_press_event', onclick)
    plt.legend()
    plt.show()
    fig.canvas.mpl_disconnect(points)
    global coords
    points = coords

    m = (points[1] - points[0]) / (points[3] - points[2])
    b = points[0] - m * points[2]
    shiftedwavelength = np.zeros(len(wavelength))
    for index, element in enumerate(np.array(wavelength).astype(float)):
        shiftedwavelength[index] = (element / m) - (b / m)

    plt.plot(wavelength, Early, 'ko', label='unshifted data')
    plt.plot(convert(statfreq), statOD, 'r-', label='stationary spectrum')
    plt.plot(shiftedwavelength, Early, 'go-', label='shifted data')
    plt.legend()
    plt.show()
    return (shiftedwavelength)


def onclick(event):
    """returns coords with the x coordinates of the positions clicked in the plot
    has to have a 'coords = []' in the global environment to work"""
    ix = event.xdata
    print('x = ', ix)
    global coords
    coords.append(ix)


def main():
    plotCrossCorrControl=False
    """ Mech Delay import"""
    path_mech = 'AvTransients_TiCp2NCs2_2022.02.25_without4ths_PixelErrorCorrected'
    tmp_mech = np.genfromtxt(path_mech + '.dat', delimiter=' ')
    delays_mech = tmp_mech[1:, 0]
    freq_mech = tmp_mech[0, 1:]
    ODs_mech = tmp_mech[1:, 1:]
    wavelength_mech = convert(freq_mech)

    """ Interdelay 1 import"""
    path_int1 = 'AvTransients_TiCp2NCS2_2022.02.21_interdelay1_without4ths'
    tmp_int1 = np.genfromtxt(path_int1 + '.dat', delimiter=' ')
    delays_int1 = tmp_int1[1:, 0]
    freq_int1 = tmp_int1[0, 1:]
    ODs_int1 = tmp_int1[1:, 1:]
    wavelength_int1 = convert(freq_int1)

    """ Interdelay 2 import"""
    path_int2 = 'AvTransients_TiCp2NCS2_2022.02.22_interdelay2'
    tmp_int2 = np.genfromtxt(path_int2 + '.dat', delimiter=' ')
    delays_int2 = tmp_int2[1:, 0]
    freq_int2 = tmp_int2[0, 1:]
    ODs_int2 = tmp_int2[1:, 1:]
    wavelength_int2 = convert(freq_int2)

    """ Elec delay import"""
    path_elec = 'AvTransients_TiCp2NCS2_2022.02.17_elecdelay_PixelErrorCorrected'
    tmp_elec = np.genfromtxt(path_elec + '.dat', delimiter=' ')
    delays_elec = tmp_elec[1:, 0]
    freq_elec = tmp_elec[0, 1:]
    ODs_elec = tmp_elec[1:, 1:]
    wavelength_elec = convert(freq_elec)

    """ find common delays"""
    common_delays_mech_inter1 = np.intersect1d(delays_mech, delays_int1)
    common_delays_inter1_inter2 = np.intersect1d(delays_int1, delays_int2)



    """ defining interpolation grid"""
    wlstepsize = 1
    wl_interp_grid = np.arange(int(np.amin(wavelength_mech)), int(np.amax(wavelength_mech)) + 2 * wlstepsize, wlstepsize)
    wavelength_common = wavelength_mech


    """ mech and inter1"""
    """ cutting out common delays"""
    ODs_mech_tointerpolate = ODs_mech[getidx(common_delays_mech_inter1, delays_mech), :]
    ODs_int1_tointerpolate = ODs_int1[getidx(common_delays_mech_inter1, delays_int1), :]

    """ interpolation on wl_interp_grid"""
    interp_mech = interpolate.interp1d(wavelength_mech, ODs_mech_tointerpolate, kind='cubic', bounds_error=False, fill_value='extrapolate')
    ODs_mech_interp = interp_mech(wl_interp_grid)
    interp_int1 = interpolate.interp1d(wavelength_int1, ODs_int1_tointerpolate, kind='cubic', bounds_error=False, fill_value='extrapolate')
    ODs_int1_interp = interp_int1(wl_interp_grid)

    if plotCrossCorrControl:
        plt.plot(wl_interp_grid, ODs_mech_interp, label='mech')
        plt.plot(wl_interp_grid, ODs_int1_interp, label='int1')
        plt.legend()
        plt.show()


    """cross correlation and wl shift determination"""
    corr = signal.correlate(ODs_mech_interp, ODs_int1_interp)
    lag = signal.correlation_lags(len(wl_interp_grid), len(wl_interp_grid))

    if plotCrossCorrControl:
        plt.plot(lag, corr)
        plt.show()

    wl_shift_int1 = (len(wl_interp_grid) - getidx(np.amax(np.abs(corr)), corr)) * wlstepsize -wlstepsize

    """ interpolation of wl shifted int1 data on mech wl grid"""
    interp2d_int1 = interpolate.interp2d(wavelength_int1 - wl_shift_int1, delays_int1, ODs_int1, kind='cubic', bounds_error=False)
    ODs_int1_wlcorr = np.fliplr(interp2d_int1(wavelength_common, delays_int1))

    """determining scaling factor """
    scaling_int1 = np.amax(np.abs(ODs_mech[getidx(common_delays_mech_inter1, delays_mech)])) / np.amax(np.abs(
        ODs_int1_wlcorr[getidx(common_delays_mech_inter1, delays_int1)]))

    if plotCrossCorrControl:
        plt.plot(wavelength_common, ODs_mech[getidx(common_delays_mech_inter1, delays_mech)], label='mech')
        plt.plot(wavelength_common, ODs_int1_wlcorr[getidx(common_delays_mech_inter1, delays_int1)] * scaling_int1, label='int1')
        plt.legend()
        plt.show()

    """ inter1 and inter2"""
    """ cutting out common delays"""
    ODs_int1_tointerpolate = ODs_int1_wlcorr[getidx(common_delays_inter1_inter2, delays_int1), :]
    ODs_int2_tointerpolate = ODs_int2[getidx(common_delays_inter1_inter2, delays_int2), :]

    """ interpolation on wl_interp_grid"""
    interp_int1 = interpolate.interp1d(wavelength_common, ODs_int1_tointerpolate, kind='cubic', bounds_error=False,
                                       fill_value='extrapolate')
    ODs_int1_interp = interp_int1(wl_interp_grid)

    interp_int2 = interpolate.interp1d(wavelength_int2, ODs_int2_tointerpolate, kind='cubic', bounds_error=False,
                                       fill_value='extrapolate')
    ODs_int2_interp = interp_int2(wl_interp_grid)

    if plotCrossCorrControl:
        plt.plot(wl_interp_grid, ODs_int1_interp, label='int1')
        plt.plot(wl_interp_grid, ODs_int2_interp, label='int2')
        plt.legend()
        plt.show()

    """cross correlation and wl shift determination"""
    corr = signal.correlate(ODs_int1_interp, ODs_int2_interp)
    lag = signal.correlation_lags(len(wl_interp_grid), len(wl_interp_grid))

    if plotCrossCorrControl:
        plt.plot(lag, corr)
        plt.show()

    wl_shift_int2 = (len(wl_interp_grid) - getidx(np.amax(np.abs(corr)), corr)) * wlstepsize - wlstepsize

    """ interpolation of wl shifted int1 data on mech wl grid"""
    interp2d_int2 = interpolate.interp2d(wavelength_int2 - wl_shift_int2, delays_int2, ODs_int2, kind='cubic',
                                         bounds_error=False)
    ODs_int2_wlcorr = np.fliplr(interp2d_int2(wavelength_common, delays_int2))

    """determining scaling factor """
    scaling_int2 =np.amax(np.abs(ODs_int1_wlcorr[getidx(common_delays_inter1_inter2, delays_int1)])) / np.amax(np.abs(ODs_int2_wlcorr[getidx(common_delays_inter1_inter2, delays_int2)]))

    if plotCrossCorrControl:
        plt.plot(wavelength_common, ODs_int1_wlcorr[getidx(common_delays_inter1_inter2, delays_int1)], label='int1')
        plt.plot(wavelength_common, ODs_int2_wlcorr[getidx(common_delays_inter1_inter2, delays_int2)] * scaling_int2, label='int2')
        plt.legend()
        plt.show()

    """int2 and elec"""
    """ cutting out common delays"""
    ODs_int2_tointerpolate = ODs_int2_wlcorr[-1, :]
    ODs_elec_tointerpolate = ODs_elec[getidx(12000, delays_elec), :]

    """ interpolation on wl_interp_grid"""
    interp_int2 = interpolate.interp1d(wavelength_common, ODs_int2_tointerpolate, kind='cubic', bounds_error=False,
                                       fill_value='extrapolate')
    ODs_int2_interp = interp_int2(wl_interp_grid)

    interp_elec = interpolate.interp1d(wavelength_elec, ODs_elec_tointerpolate, kind='cubic', bounds_error=False,
                                       fill_value=0)
    ODs_elec_interp = interp_elec(wl_interp_grid)

    if plotCrossCorrControl:
        plt.plot(wl_interp_grid, ODs_int2_interp, label='int2')
        plt.plot(wl_interp_grid, ODs_elec_interp, label='elec')
        plt.legend()
        plt.show()

    """cross correlation and wl shift determination"""
    corr = signal.correlate(ODs_int2_interp, ODs_elec_interp)
    lag = signal.correlation_lags(len(wl_interp_grid), len(wl_interp_grid))

    if plotCrossCorrControl:
        plt.plot(lag, corr)
        plt.show()

    wl_shift_elec = (len(wl_interp_grid) - getidx(np.amax(np.abs(corr)), corr)) * wlstepsize -wlstepsize

    """ interpolation of wl shifted int1 data on mech wl grid"""
    interp2d_elec = interpolate.interp2d(wavelength_elec - wl_shift_elec, delays_elec, ODs_elec, kind='cubic',
                                         bounds_error=False)
    ODs_elec_wlcorr = np.fliplr(interp2d_elec(wavelength_common, delays_elec))

    """determining scaling factor """
    scaling_elec = np.amax(np.abs(ODs_int2_wlcorr[-1])) / np.amax(np.abs(ODs_elec_wlcorr[getidx(12000, delays_elec)]))

    if plotCrossCorrControl:
        plt.plot(wavelength_common, ODs_int2_wlcorr[-1], label='int2')
        plt.plot(wavelength_common, ODs_elec_wlcorr[getidx(12000, delays_elec)]*scaling_elec, label='elec')
        plt.legend()
        plt.show()
        plt.plot(wavelength_common, ODs_mech[getidx(0, delays_mech)], label='mech, t = 0')
        plt.plot(wavelength_common, ODs_elec_wlcorr[getidx(0, delays_elec)]*scaling_elec, label='elec, t = 0')
        plt.legend()
        plt.show()

    """ cut data to remove before 0 for electronic  and overlapping delays"""
    ODs_int1_wlcorr_del = np.delete(ODs_int1_wlcorr, 0, 0)
    delays_int1_del = delays_int1[1:]
    ODs_int2_wlcorr_del = np.delete(ODs_int2_wlcorr, [0,1], 0)
    delays_int2_del = delays_int2[2:]
    ODs_elec_wlcorr_del = np.delete(ODs_elec_wlcorr, np.s_[0:(getidx(0, delays_elec)+1)], 0)
    delays_elec_del = delays_elec[(getidx(0, delays_elec)+1):]
    ODs_elec_wlcorr_del = np.delete(ODs_elec_wlcorr_del, np.s_[getidx(4630000, delays_elec_del):(getidx(7070000, delays_elec_del)+1)], 0)
    delays_elec_del = np.delete(delays_elec_del, np.s_[getidx(4630000, delays_elec_del):(getidx(7070000, delays_elec_del)+1)])

    """ merge all data"""
    ODs_complete = np.concatenate((ODs_mech, ODs_int1_wlcorr_del * scaling_int1, ODs_int2_wlcorr_del * scaling_int2 * scaling_int1, ODs_elec_wlcorr_del * scaling_elec), axis=0)
    delays_complete = np.hstack((delays_mech, delays_int1_del, delays_int2_del, delays_elec_del))

    """ wavelength calibration"""
    wavelength_common = linearwavelengthshift(ODs_complete, wavelength_common, delays_complete,
                                      statspectraname='TiCp2NCS2_FTIR', timetowatch=0)
    freq_common = convert(wavelength_common)

    """ plotting"""
    #Transients = (2025, 2063, 1998, 2044, 2008, 2087)
    #plottransientlog(ODs_complete, freq_common, delays_complete, Transients)
    #plotting(ODs_complete, freq_common, delays_complete)
    #plottingmesh(np.arcsinh(8*ODs_complete), freq_common, delays_complete)
    #Transientspectra=(1, 2, 4, 6, 10, 20, 30, 50, 100)
    #for line in Transientspectra:
    #    plotTransSpec(ODs_complete, freq_common, delays_complete, line)
    #plt.legend()
    #plt.show()
    #Transientspectra = (150, 266, 256, 780, 2300, 2800, 4500, 8600)
    #for line in Transientspectra:
    #    plotTransSpec(ODs_complete, freq_common, delays_complete, line)
    #plt.legend()
    #plt.show()
    #Transientspectra = (50000, 200000, 800000, 15000000,12000000, 40000000, 60000000, 100000000, 200000000, 300000000)
    #for line in Transientspectra:
    #    plotTransSpec(ODs_complete, freq_common, delays_complete, line)
    #plt.legend()
    #plt.show()


    output('CombinedAvTransients', freq_common, delays_complete, ODs_complete)
    output('CombinedAvTransientSpectra', delays_complete, freq_common, np.transpose(ODs_complete))



if __name__ == '__main__':
    coords=[]
    main()