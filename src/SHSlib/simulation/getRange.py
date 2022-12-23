def getRange(A, margin=0.2):
    import numpy as np

    Amin = np.min(A) - (margin * A[-1] - A[0])
    Amax = np.max(A) + (margin * A[-1] - A[0])
    return Amin, Amax
