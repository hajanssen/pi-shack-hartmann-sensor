def gauss(x, sig, mu):
    import numpy as np

    a = (1 / np.sqrt(2 * np.pi * sig**2)) * np.exp(-((x - mu) ** 2) / (2 * sig**2))
    return a
