import matplotlib.pyplot as plt


def visualize(class_object, pause_time=0.5):
    subplots = list()

    plt.ion()
    fig, ax = plt.subplots(4, 4, sharey=True)
    subplots.append(plt.subplot(4, 2, 1))
    subplots.append(plt.subplot(4, 2, 2))
    subplots.append(plt.subplot(4, 2, 3))
    subplots.append(plt.subplot(4, 2, 4))
    subplots.append(plt.subplot(2, 1, 2))

    subplots[4].set_xlabel("wavelength / nm")

    for idx_run in range(class_object.no_runs):
        for delay in class_object.cleared_data_sb[idx_run][0].index:

            subplots[4].clear()
            for idx_st_run in range(class_object.no_st_runs):
                subplots[idx_st_run].clear()
                subplots[idx_st_run].plot(class_object.raw_data_sb[idx_run][idx_st_run].columns,
                                          class_object.raw_data_sb[idx_run][idx_st_run].loc[delay, :], marker="o",
                                          label="raw data")
                subplots[idx_st_run].plot(class_object.cleared_data_sb[idx_run][idx_st_run].columns,
                                          class_object.cleared_data_sb[idx_run][idx_st_run].loc[delay, :], marker="o",
                                          label="cleared data")
                subplots[idx_st_run].legend()


            subplots[4].plot(class_object.raw_data_merged[idx_run].columns, class_object.raw_data_merged[idx_run].loc[delay, :],
                             label="raw data")
            subplots[4].plot(class_object.cleared_data_merged[idx_run].columns, class_object.cleared_data_merged[idx_run].loc[delay, :],
                             label="cleared data")
            subplots[4].legend(loc="lower right")

            subplots[4].set_xlabel("wavelength / nm")

            fig.suptitle("delay: " + str(delay) + " ps", fontsize=26)

            plt.pause(pause_time)
            plt.draw()
