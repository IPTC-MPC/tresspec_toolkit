from ninevski_oleary import *
from scipy.optimize import minimize

def sinlge_sided(x_l, y_l, d_l, x_r, y_r, d_r, n, f_sc, offset, return_arg="tn_fg"):

    func = lambda mb: ninevski_oleary(x_l, y_l, d_l, x_r, mb[0] * y_r + mb[1], d_r, n)

    res1 = minimize((func([f_sc, offset])[2]), x0=[2.0, 0.4], metho="SLSQP")


# def two_sided
#
#     # build Vandermonde matrices
#     V_L = np.vander(x_l, d_l + 1)
#     V_R = np.vander(x_r, d_r + 1)
#
#     y_r = np.vander(np.squeeze(y_r), 2) @ np.array([[f_sc], [offset]])
#
#     y = np.vstack((y_l, y_r))
#
#     # build V matrix from Vandermonde matrices
#     V = linalg.block_diag(V_L, V_R)
#
#     # build C matrix
#     C = np.hstack((np.zeros((n, d_l + 1 - n)), np.identity(n), np.zeros((n, d_r + 1 - n)), -np.identity(n)))
#     C = np.atleast_2d(C)
#
#     # calculate orthonormal vector basis of null(C),
#     # i.e. basis vector for the vector space whose elements multiplied with C always return the zero vector
#     N = linalg.null_space(C)
#
#     gamma = N @ linalg.pinv(V @ N) @ y
#
#     # split to extract alpha and beta
#     alpha = np.atleast_2d(gamma[:d_l + 1])
#     beta = np.atleast_2d(gamma[d_l + 1:])
#
#
#     tn_fg = abs(alpha[-(n+1)][0] - beta[-(n+1)][0])
#
#     # calculate errors
#     # c.f. Section 4.1 (approximation error)
#     E_a = (y_l - V_L @ alpha).T @ (y_l - V_L @ alpha) + (y_r - V_R @ beta).T @ (y_r - V_R @ beta)
#
#     # c.f. Section 4.3 (extrapolation error)
#     E_e = (y_l - V_L @ beta).T @ (y_l - V_L @ beta) + (y_r - V_R @ alpha).T @ (y_r - V_R @ alpha)
#
#     print(f"Taylor coefficients (alpha):\n{alpha}")
#     print(f"Taylor coefficients (beta):\n{beta}")
#
#     print(f"tn_fg = {tn_fg}")
#     print(f"approximation error (E_a) = {E_a[0][0]}")
#     print(f"extrapolation error (E_e) = {E_e[0][0]}")
#
#     if return_arg == "tn_fg":
#         return tn_fg
#     elif return_arg == "E_a":
#         return E_a[0][0]
#     else:
#         return E_e[0][0]
