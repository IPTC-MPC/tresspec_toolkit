import pandas as pd
from tresspec_toolkit.process.revive_dead_pixels.ninevski_oleary import *
from scipy.optimize import minimize


def get_left_and_right_data(*args, sb=4, intact_pixels=1, intact="left"):
    """

    :param args:
    :param sb:
    :param intact_pixels:
    :param intact:
    :return:
    """

    dead_pixel_idx = args[-1]
    if len(args) == 3:
        x = args[0]
        y = args[1]
    else:
        x = args[0].index
        y = args[0].to_numpy().squeeze()

    ################################################
    if intact == "right":
        idx_l = [i for i in range(dead_pixel_idx * sb, (dead_pixel_idx + intact_pixels) * sb)]      # the intact pixel(s)
        idx_r = [i for i in range((dead_pixel_idx - 1) * sb, dead_pixel_idx * sb)]  # the dead pixel
    else:
        # take intact pixel from the left
        idx_l = [i for i in range((dead_pixel_idx-1-intact_pixels)*sb, (dead_pixel_idx-1) * sb)]
        idx_r = [i for i in range((dead_pixel_idx-1)*sb, dead_pixel_idx * sb)]


    # grep the left and right sided data
    x_l, x_r = np.atleast_2d(x[idx_l]).T, np.atleast_2d(x[idx_r]).T

    #y_l, y_r = y[idx_l], y[idx_r]

    y_l, y_r = np.atleast_2d(y[idx_l]).T, np.atleast_2d(y[idx_r]).T

    #y_r = ,

    x00 = np.mean([x_l[-1], x_r[0]]) if intact == "left" else np.mean([x_r[-1], x_l[0]])

    x_l, x_r = x_l - x00, x_r - x00

    return x_l, y_l, x_r, y_r, x00


def sinlge_sided(x_l, y_l, d_l, x_r, y_r, d_r, n):  #, f_sc, offset, return_arg="tn_fg"

    # wrapper_func = lambda mb: ninevski_oleary(x_l, y_l, d_l, x_r, mb[0] * y_r + mb[1], d_r, n)[2]
    def wrapper_func(beta):
        return ninevski_oleary(x_l, y_l, d_l, x_r, beta[0] * y_r + beta[1], d_r, n)[2]  # lambda mb:

    res1 = minimize(wrapper_func, x0=np.array([2.0, 0.4]), method="SLSQP")

    return res1


def two_sided(x_l1, y_l1, d_l1, x_r1, y_r1, d_r1, x_l2, y_l2, d_l2, x_r2, y_r2, d_r2, n):

    #wrapper_func1 = lambda mb: np.sqrt(ninevski_oleary(x_l1, y_l1, d_l1, x_r1, mb[0] * y_r1 + mb[1], d_r1, n)[2]**2 +
    #                                   ninevski_oleary(x_l2, y_l2, d_l2, x_r2, mb[0] * y_r2 + mb[1], d_r2, n)[2]**2)

    def wrapper_func(mb):
        return np.sqrt(ninevski_oleary(x_l1, y_l1, d_l1, x_r1, mb[0] * y_r1 + mb[1], d_r1, n)[2] ** 2 +
                       ninevski_oleary(x_l2, y_l2, d_l2, x_r2, mb[0] * y_r2 + mb[1], d_r2, n)[2] ** 2)

    res1 = minimize(wrapper_func, x0=np.array([2.0, 0.4]), method="SLSQP", bounds=[(1, np.inf), (None, None)])

    return res1
