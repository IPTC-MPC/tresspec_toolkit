# function definition as devised in
#  - Wezisla, B.; Lindner, J.; Das, U.; Filippou, A. C.; Vöhringer, P. Angew. Chem., Int. Ed. 2017, 56, 6901–6905.
#  - D. B. Siano, D. E. Metzler, The Journal of Chemical Physics 1969, 51, 1856-1861

import numpy as np


def lognormal(nu, a, nu0, delta, rho):
    alpha = nu0 + delta * rho / (rho ** 2 - 1)
    gamma = np.log(rho) / np.sqrt(2 * np.log(2))
    beta = np.exp(gamma ** 2) * (alpha - nu0)

    def lognorm(nu_2):
        dod_2 = a * ((alpha - nu_2) * gamma * np.exp(-gamma ** 2 / 2)) ** -1 * np.exp(-1 / (2 * gamma ** 2) *
                                                                                      (np.log(
                                                                                          (alpha - nu_2) / beta)) ** 2)
        return dod_2

    dod1 = lognorm(nu[nu < alpha])
    dod2 = 0 * np.array(nu[nu >= alpha])

    dod = np.concatenate((dod1, dod2), axis=0)

    return dod
