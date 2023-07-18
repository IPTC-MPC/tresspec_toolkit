import numpy as np
from scipy import linalg


def ninevski_oleary(x_l, y_l, d_l, x_r, y_r, d_r, n, f_sc, offset, return_arg="tn_fg"):
    """
    An algorithm to detect Cn discontinuities based on the publication by Ninevski and O'Leary
    :param x_l:         the left-sided x values
    :param y_l:         the left-sided y values
    :param d_l:         the polynomial degree of the Taylor approximation to the left-sided data
    :param x_r:         the right-sided x values
    :param y_r:         the right-sided y values
    :param d_r:         the polynomial degree of the Taylor approximation to the right-sided data
    :param n:           specifying the order of the derivative to check for discontinuity
    :return:            tn_fg: the difference in the Taylor coefficients (alpha_n - beta_n)
                        E_a: the error of approximation (deviation between fits and corresponding actual data)
                        E_e: the error of extrapolation (deviation between extrapolated fits and actual data)
    """

    # build Vandermonde matrices
    V_L = np.vander(x_l.squeeze(), d_l + 1)
    V_R = np.vander(x_r.squeeze(), d_r + 1)

    y_r = np.vander(np.squeeze(y_r), 2) @ np.array([[f_sc], [offset]])

    y = np.vstack((np.atleast_2d(y_l).T,
                   np.atleast_2d(y_r).T))

    # build V matrix from Vandermonde matrices
    V = linalg.block_diag(V_L, V_R)

    # build C matrix
    C = np.hstack((np.zeros((n, d_l + 1 - n)), np.identity(n), np.zeros((n, d_r + 1 - n)), -np.identity(n)))
    C = np.atleast_2d(C)

    # calculate orthonormal vector basis of null(C),
    # i.e. basis vector for the vector space whose elements multiplied with C always return the zero vector
    N = linalg.null_space(C)

    gamma = N @ linalg.pinv(V @ N) @ y

    # split to extract alpha and beta
    alpha = np.atleast_2d(gamma[:d_l + 1])
    beta = np.atleast_2d(gamma[d_l + 1:])

    tn_fg = abs(alpha[-(n + 1)][0] - beta[-(n + 1)][0])

    # calculate errors
    # c.f. Section 4.1 (approximation error)
    E_a = (y_l - V_L @ alpha).T @ (y_l - V_L @ alpha) + (y_r - V_R @ beta).T @ (y_r - V_R @ beta)

    # c.f. Section 4.3 (extrapolation error)
    E_e = (y_l - V_L @ beta).T @ (y_l - V_L @ beta) + (y_r - V_R @ alpha).T @ (y_r - V_R @ alpha)

    print(f"Taylor coefficients (alpha):\n{alpha}")
    print(f"Taylor coefficients (beta):\n{beta}")

    print(f"tn_fg = {tn_fg}")
    print(f"approximation error (E_a) = {E_a[0][0]}")
    print(f"extrapolation error (E_e) = {E_e[0][0]}")

    return tn_fg, E_a, E_e
