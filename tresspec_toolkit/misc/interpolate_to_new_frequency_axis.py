

def interpolate_to_new_frequency_axis(df1, reference, delta_lambda=0.0, kind="cubic"):

    """
    
    :param df1:          the data whose frequency axis is to be reinterpolated
    :param reference:    the data set that provides the new frequency axis
    :param delta_lambda: a shift to account for an offset in the frequency axis of 'df1'
    :param kind:         the type of interpolation scheme to be used ("linear", "cubic", "quintic"); defaults to "cubic"
    :return: 
    """

    from scipy.interpolate import interp2d
    import pandas as pd

    ####################################################################################################################
    # create instance of scipy.interpolate.interp2d class
    try:
        f = interp2d(df1.columns, 10**7/(10**7/df1.index + delta_lambda), df1.to_numpy(), kind=kind)
    except ValueError:
        print("Invalid type of interpolation provided. Using default 'cubic' interpolation scheme")
        f = interp2d(df1.columns, df1.index + delta_lambda, df1.to_numpy(), kind="cubic")

    ####################################################################################################################
    # interpolate to new frequency axis
    df1_interpolated = f(df1.columns, reference.index)

    df1_interpolated = pd.DataFrame(df1_interpolated, index=reference.index, columns=df1.columns)

    return df1_interpolated
