import matplotlib.pyplot as plt


def visualize(run_sb, wavelength, denoised_data, pause_time=0.1):
    subplots = list()

    plt.ion()
    fig, ax = plt.subplots(4, 4, sharey=True)
    subplots.append(plt.subplot(4, 2, 1))
    subplots.append(plt.subplot(4, 2, 2))
    subplots.append(plt.subplot(4, 2, 3))
    subplots.append(plt.subplot(4, 2, 4))
    subplots.append(plt.subplot(2, 1, 2))

    subplots[4].set_xlabel("wavelength / nm")

    print("indices:")
    print(run_sb[0].index)
    for delay in run_sb[0].index:
        subplots[4].clear()
        for idx, sb in enumerate(run_sb):
            subplots[idx].clear()
            subplots[idx].plot(sb.columns, sb.loc[delay, :], marker="o")

            subplots[4].plot(sb.columns, sb.loc[delay, :], marker="o", linestyle="None")


        subplots[4].plot(wavelength, denoised_data)
        subplots[4].set_xlabel("wavelength / nm")

        fig.suptitle("delay: " + str(delay) + " ps", fontsize=26)

        plt.pause(pause_time)
        plt.draw()
