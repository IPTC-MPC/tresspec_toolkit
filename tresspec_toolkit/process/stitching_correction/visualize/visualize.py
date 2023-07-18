import matplotlib.pyplot as plt


def visualize(class_object, pause_time=0.5):
    subplots = list()

    plt.ion()
    fig, ax = plt.subplots(sharey=True)
    subplots.append(plt.subplot(5, 2, 1))
    subplots.append(plt.subplot(5, 2, 2))
    subplots.append(plt.subplot(5, 2, 3))
    subplots.append(plt.subplot(5, 2, 4))
    subplots.append(plt.subplot(5, 1, (3, 4)))
    subplots.append(plt.subplot(5, 1, 5))

    subplots[4].set_xlabel("wavelength / nm")

    for idx_run in range(class_object.no_runs):
        for delay in class_object.cleared_data_sb[idx_run][0].index:

            subplots[4].clear()
            subplots[5].clear()
            for idx_st_run in range(class_object.no_st_runs):
                subplots[idx_st_run].clear()
                subplots[idx_st_run].plot(class_object.raw_data_sb[idx_run][idx_st_run].columns,
                                          class_object.raw_data_sb[idx_run][idx_st_run].loc[delay, :], marker="o",
                                          label="raw data")
                subplots[idx_st_run].plot(class_object.cleared_data_sb[idx_run][idx_st_run].columns,
                                          class_object.cleared_data_sb[idx_run][idx_st_run].loc[delay, :], marker="o",
                                          label="cleared data")
                # subplots[idx_st_run].legend()


            subplots[4].plot(class_object.raw_data_merged[idx_run].columns, class_object.raw_data_merged[idx_run].loc[delay, :],
                             label="raw data")
            subplots[4].plot(class_object.cleared_data_merged[idx_run].columns, class_object.cleared_data_merged[idx_run].loc[delay, :],
                             label="cleared data")
            subplots[4].legend(loc="lower right", frameon=False, labelcolor='linecolor', handlelength=0.0)

            subplots[5].plot(class_object.raw_data_merged[idx_run].columns,
                             class_object.raw_data_merged[idx_run].loc[delay, :] -
                             class_object.cleared_data_merged[idx_run].loc[delay, :],
                             label="residuals", color="r")


            subplots[5].set_xlabel("wavelength / nm")



            fig.suptitle("t =  " + str(delay) + " ps (run " + str(idx_run+1) + " of " +
                         str(class_object.no_runs) + ")", fontsize=26)

            plt.pause(pause_time)
            plt.draw()
