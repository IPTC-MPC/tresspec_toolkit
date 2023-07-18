import copy


def create_dg535_time_axis(runs, runs_sb=None, zero_step=7, time_increment=11.83, drop_steps=[]):

    """

    :param runs:            a list containing the runs compiled as pandas DataFrames
    :param runs_sb:         a list of lists containing the individual stitching runs as pandas DataFrames
    :param zero_step:       the time step in which pump and probe hit the sample at the same time
    :param time_increment:  the time increment between successive steps (should be 11.83 ns)
    :param drop_steps:      a list containing the steps which are corrupted and should therefore be omitted (optional)
    :return:
    """

    runs_proper_t_axis = list()
    runs_sb_proper_t_axis = list()

    if not isinstance(drop_steps, list):
        drop_steps = [drop_steps]
    runs_w_corr_t_axis = list()
    runs_w_corr_t_axis_sb = list()

    # setting for runs
    for run in runs:

        runs_proper_t_axis.append(run.drop(columns=drop_steps))
        runs_proper_t_axis[-1].columns = (runs_proper_t_axis[-1].columns - zero_step) * time_increment

    for run_sb in runs_sb:
        sb_sub_tmp = list()
        for sb in run_sb:

            sb_sub_tmp.append(sb.drop(index=drop_steps))
            sb_sub_tmp[-1].index = (sb_sub_tmp[-1].index - zero_step) * time_increment

        runs_sb_proper_t_axis.append(sb_sub_tmp)

    return runs_proper_t_axis, runs_sb_proper_t_axis
