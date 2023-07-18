from tresspec_toolkit.process.revive_dead_pixels.slope_fixing import *
from tresspec_toolkit.process.revive_dead_pixels.manipulate_pixel import *


def revive_dead_pixel(*args, sb=4, intact_pixels=1, mode="two-sided", d_l=3, d_r=3, n=1):
    """
    adding a docstring here later on
    :param args:
    :param sb:
    :param intact_pixels:
    :param mode:
    :param d_l:
    :param d_r:
    :param n:
    :return:
    """

    # TODO: test with simulated pump-probe spectra
    #  if that works fine, then wrap this thing into a more general function handling a pointer array to dead pixels!

    dead_pixel_idx = args[-1]
    if len(args) == 3:
        x = args[0]
        y = args[1]
    else:
        x = args[0].index
        y = args[0].to_numpy().squeeze()

    # draw the values and determine the optimal scaling values
    if mode == "left-sided":
        x_good_l, y_good_l, x_bad_l, y_bad_l, _ = get_left_and_right_data(x, y, dead_pixel_idx, sb=sb,
                                                                          intact_pixels=intact_pixels, intact="left")

        res = sinlge_sided(x_good_l, y_good_l, d_l, x_bad_l, y_bad_l, d_r, n)
    elif mode == "right-sided":
        x_good_l, y_good_l, x_bad_l, y_bad_l, _ = get_left_and_right_data(x, y, dead_pixel_idx, sb=sb,
                                                                          intact_pixels=intact_pixels, intact="right")

        res = sinlge_sided(x_good_l, y_good_l, d_l, x_bad_l, y_bad_l, d_r, n)
    else:
        x_good_l, y_good_l, x_bad_l, y_bad_l, _ = get_left_and_right_data(x, y, dead_pixel_idx, sb=sb,
                                                                          intact_pixels=intact_pixels, intact="left")
        x_good_r, y_good_r, x_bad_r, y_bad_r, _ = get_left_and_right_data(x, y, dead_pixel_idx, sb=sb,
                                                                          intact_pixels=intact_pixels, intact="right")

        res = two_sided(x_good_l, y_good_l, d_l, x_bad_l, y_bad_l, d_r,
                        x_good_r, y_good_r, d_l, x_bad_r, y_bad_r, d_r, n)

    data_corrected = manipulate_pixel(y, dead_pixel_idx, *res.x, sb=sb)

    return data_corrected
