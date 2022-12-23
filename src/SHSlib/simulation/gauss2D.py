def gauss2D(x, y, dx, dy, sx=0.5, sy=0.5):
    import numpy as np
    from . import gauss

    x = gauss(x, sx, dx)
    y = gauss(y, sy, dy)

    c = np.zeros((len(x), len(y)))

    for i in range(0, len(x)):
        c[i, :] = x[i] * y
    return c
