

def set_time_axis_for_intermediate_measurements(datasets, tau_long_pump_path, tau_shortened_pump_path_1,
                                                tau_shortened_pump_path_2=None, tau_even_shorter_pump_path=None):

    """
    A function to generate the correct delay axis based on the shortening of the pump path
    (applying approach to make time regime in between mechanical and electronic delay accessible (3.5 ns to 11.83 ns))

    :param datasets:                    a list containing the datasets as pandas DataFrames
    :param tau_long_pump_path:          the delay measured between the probe and the pump in the regular optical setup
    :param tau_shortened_pump_path_1:   delay measured with pump path shortened by a certain smaller amount (1st step)
    :param tau_shortened_pump_path_2:   delay measured with pump path shortened by a certain smaller amount (2nd step)
    :param tau_even_shorter_pump_path:  the delay measured with pump path shortened by a certain larger amount
    :return:                            a list containing the measurements with the time axes properly set
    """

    try:
        time_offset = (tau_long_pump_path - tau_shortened_pump_path_1) +\
                      (tau_shortened_pump_path_2 - tau_even_shorter_pump_path)
    except TypeError:
        time_offset = (tau_long_pump_path - tau_shortened_pump_path_1)

    datasets_t_axis_set = list()

    for dataset in datasets:
        datasets_t_axis_set.append(dataset)
        datasets_t_axis_set[-1].columns += time_offset

    return datasets_t_axis_set
