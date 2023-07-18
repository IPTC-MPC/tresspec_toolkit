import numpy as np
from scipy.linalg import lstsq
from sklearn.metrics import mean_squared_error


def determine_linear_scaling(df1, reference, print_results=False):
    """

    :param df1:         the data to be scaled to the other set ot data
    :param reference:   the data used as reference
    :return:
    """
    if print_results:
        print(f"Performing automatic determination of scaling coefficients.")
        print(f"Assuming a linear dependence (i.e. offset + scaling factor)")

    # flatten the data
    a = df1.to_numpy().flatten()
    b = reference.to_numpy().flatten()

    design_matrix = np.vander(a, 2)

    beta = lstsq(design_matrix, np.atleast_2d(b).T)

    # calculate the RMSE between reference and scaled data
    rmse = mean_squared_error(b, design_matrix @ beta[0])**0.5

    # dump fit parameters in a list for further usage in function 'intensity_scaling'
    results = [i[0] for i in beta[0]]

    ####################################################################################################################
    # df1_scaled = df1 * beta[0] + np.ones_like(df1) * beta[1]

    if print_results:
        print("\n")
        print(f"Residuals of linear regression: {beta[1][0]}")
        print(f"Root mean squared error (ref. vs. scaled): {rmse}")
        print("beta: ", results)
        print("\n")

    return results, rmse
