def make1D(A):
    import numpy as np

    return np.reshape(A, A.shape[0] * A.shape[1])
