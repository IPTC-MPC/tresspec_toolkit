import numpy as np


def total_variation(data):
    # Calculate the n - th discrete difference along the given axis.
    # The first difference is given by out[i] = a[i + 1] - a[i]

    tv = sum(abs(np.diff(data)))
    return tv




def dod_sim_noisy(dod, noise, pixel2pixel_noise=None):

    if pixel2pixel_noise is None:
        pixel2pixel_noise = [0, 0, 0, 0]

    wns, delays = dod.shape

    noise_mat = np.tile(np.array(noise), (delays, int(wns/4))).transpose()

    # pixel-to-pixel noise
    p2p_noise = np.concatenate((np.array(pixel2pixel_noise), -np.array(pixel2pixel_noise)))
    p2p_noise = np.tile(p2p_noise, (delays, int(wns/8))).transpose()

    print(noise_mat.shape)
    dod_noisy = dod + noise_mat + p2p_noise
    return dod_noisy


def dod_sim(freq, delays, paras_lognorm, paras_gauss, tau):
    """ Simulate pump-probe spectrum assumning lognormal lineshpape for absorption and gaussian lineshape for bleach

    Args:
        freq:           wavenumber axis.
        paras_lognorm:  parameters of lognormal line shape (4 component vector: nu0, a, delta, rho).
        paras_gauss:    parameters of gaussian line shape (4 component vector: a, nu0, sigma, y0.
        delays:         delay axis.
        tau:            time constant of exponential decay.

    Returns:
        dod:            Simulated pump-probe spectrum
    """

    def lognormal(nu, nu0, a, delta, rho):
        alpha = nu0 + delta * rho/(rho**2 - 1)
        gamma = np.log(rho)/np.sqrt(2*np.log(2))
        beta = np.exp(gamma**2)*(alpha - nu0)

        def lognorm(nu_2):
            dod_2 = a * ((alpha-nu_2) * gamma * np.exp(-gamma**2 / 2))**-1 * np.exp(-1/(2*gamma**2) *
                                                                                    (np.log((alpha - nu_2)/beta))**2)
            return dod_2

        dod1 = lognorm(nu[(nu[:, 0] < alpha), :])
        dod2 = 0 * np.array(nu[(nu[:, 0] >= alpha), :])

        dod = np.concatenate((dod1, dod2), axis=0)

        return dod

    def gaussian(nu, a, nu0, sigma, y0):
        return a * np.exp(-((nu - nu0) / sigma) ** 2) + y0

    return (lognormal(freq, *paras_lognorm) - gaussian(freq, *paras_gauss)) * np.exp(-delays/tau)


def lognormal(nu, nu0, a, delta, rho):
    alpha = nu0 + delta * rho/(rho**2 - 1)
    gamma = np.log(rho)/np.sqrt(2*np.log(2))
    beta = np.exp(gamma**2)*(alpha - nu0)

    def lognorm(nu_2):
        dod_2 = a * ((alpha-nu_2) * gamma * np.exp(-gamma**2 / 2))**-1 * np.exp(-1/(2*gamma**2) * (np.log((alpha - nu_2)/beta))**2)
        return dod_2


    dod1 = lognorm(nu[:, (nu[0, :] < alpha)])
    dod2 = 0 * np.array(nu[:, (nu[0, :] >= alpha)])

    dod = np.concatenate((dod1, dod2), axis=1)

    return dod

