import matplotlib.pyplot as plt


def visualize_class(results, idx_run, delay, pause_time=0.1):

    """

    :param results:     a object of the DataStitchingNoiseReduced class as defined in reduce_stitching_noise function
    :param idx_run:     the index of the run
    :param delay:       the delay to be plotted
    :param pause_time:
    :return:
    """

    subplots = list()

    # creating plot
    plt.ion()
    fig, ax = plt.subplots(4, 4, sharey=True)
    subplots.append(plt.subplot(4, 2, 1))
    subplots.append(plt.subplot(4, 2, 2))
    subplots.append(plt.subplot(4, 2, 3))
    subplots.append(plt.subplot(4, 2, 4))
    subplots.append(plt.subplot(2, 1, 2))

    subplots[4].set_xlabel("wavelength / nm")

#    for delay in delays:
#        subplots[4].clear()
    for idx_st_run in range(results.no_st_runs):
        subplots[idx_st_run].clear()

        # plot of the raw data
        subplots[idx_st_run].plot(results.raw_data_sb[idx_run][idx_st_run].columns,
                                  results.raw_data_sb[idx_run][idx_st_run].loc[delay, :], marker="o")
        # plot of denoised data
        subplots[idx_st_run].plot(results.cleared_data_sb[idx_run][idx_st_run].columns,
                                  results.cleared_data_sb[idx_run][idx_st_run].loc[delay, :], marker="o")


#        subplots[4].plot(sb.columns, sb.loc[delay, :], marker="o", linestyle="None")

    subplots[4].plot(results.raw_data[idx_run].columns, results.raw_data[idx_run].loc[delay, :])
    subplots[4].set_xlabel("wavelength / nm")

    fig.suptitle("delay: " + str(delay) + " ps", fontsize=26)

    plt.pause(pause_time)
    plt.draw()
