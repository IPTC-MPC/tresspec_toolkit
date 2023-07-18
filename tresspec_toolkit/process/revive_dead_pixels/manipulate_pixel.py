import numpy as np
import pandas as pd


def manipulate_pixel(data, pixel, f_sc, offset, sb=4, ):
    """

    :param data:    the data that contain that one pixel that should be affected
    :param pixel:   the index of the pixel to manipulate
    :param f_sc:    the scaling factor
    :param offset:
    :param sb:
    :return:
    """

    if not isinstance(pixel, int):
        pixel = int(pixel)

    modified_data = np.diag(np.array([f_sc if i in range((pixel - 1) * sb, pixel * sb) else 1 for i in range(len(data))]))\
                    @ data + np.array([offset if i in range((pixel-1) * sb, pixel * sb) else 0 for i in range(len(data))])

    return modified_data
