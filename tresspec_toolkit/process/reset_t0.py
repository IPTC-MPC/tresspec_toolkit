from scipy.interpolate import interp2d



def reset_t0(datasets, t0=0.0):
    """

    :param datasets:
    :param t0:
    :return:
    """

    if not isinstance(datasets, list):
        datasets = [datasets]

    if isinstance(t0, float):
        t0 = [t0] * len(datasets)

    dataset_t0_reset = list()

    for t_0, data in zip(t0, datasets):


        #tau_old = data.columns.
        #tau_new
        # dod

        dod = data.to_numpy()


        dataset_t0_reset.append(data)
        dataset_t0_reset[-1].columns = dataset_t0_reset[-1].columns - t_0

        # f = interp2d()

    return dataset_t0_reset
