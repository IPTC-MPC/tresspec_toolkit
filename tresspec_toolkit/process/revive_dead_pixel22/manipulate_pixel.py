import numpy as np
import pandas as pd



def mainpulate_pixel(data, pixel, f_sc, offset):

    if not isinstance(pixel, int):
        pixel = int(pixel)

    modified_data = np.diag(np.array([f_sc if i in range(int((pixel - 1) * 4), int(pixel) * 4) else 1 for i in range(128)]))\
                    @ data + np.array([offset if i in range(int((pixel-1)*4), int(pixel)*4) else 0 for i in range(128)])

    return modified_data