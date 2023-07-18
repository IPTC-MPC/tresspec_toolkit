import pandas as pd


def merge_dataset_very_basic(dataset_red, dataset_blue, f_sc = 1.0):

    """

    :param dataset_red:
    :param dataset_blue:
    :param f_sc:
    :return:
    """

    dataset_blue_sub = dataset_blue.iloc[dataset_blue.index > max(dataset_red.index):]

    merged = pd.concat(dataset_red, f_sc * dataset_blue_sub, axis=0)

    return merged