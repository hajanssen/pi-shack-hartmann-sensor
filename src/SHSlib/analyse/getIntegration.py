def getIntegration(Xn, Yn, Xpos, Ypos, NPartner=10):
    # Paramether
    # Xn : X-Position for integration point
    # Yn : Y-Position for integration point
    # Xpos: X-Position of Gradient data
    # Ypos: Y-Position of Gradient data

    P = NPartner
    import numpy as np

    # Index where Y-Component start in array "C"
    K = len(Xpos)

    C = np.zeros((2 * K, len(Xn)))

    # loop over all koordinates
    for i, (xk, yk) in enumerate(zip(Xpos, Ypos)):

        # calculate distance to dots
        dX = xk - Xn
        dY = yk - Yn

        # get index of closest points
        distance = np.sqrt(np.square(dX) + np.square(dY))
        distance_idx = np.argsort(distance)

        # distance to closest points
        dX = Xn[distance_idx[0:P]] - xk
        dY = Yn[distance_idx[0:P]] - yk

        # --- X Components ---
        # taylor series Matrix
        M = np.array(
            [np.ones(len(dX)), dX, dY, (dX**2) / 2, dX * dY, (dX**2) / 2]  # ])
        )

        # "Zero" Array with the number of Taylor polinom
        V = np.zeros((np.size(M, 0), 1))
        V[1] = 1

        # M_pinv = np.linalg.pinv(M)

        # C[i,distance_idx[0:P]] = (M_pinv @ V).T
        C[i, distance_idx[0:P]] = np.linalg.lstsq(M, V, rcond=None)[0].T
        # "Zero" Array with the number of Taylor polinom
        V = np.zeros((np.size(M, 0), 1))
        V[2] = 1
        # C[i+K,distance_idx[0:P]] = (M_pinv @ V).T
        C[i + K, distance_idx[0:P]] = np.linalg.lstsq(M, V, rcond=None)[0].T

    empty_row = np.zeros((C.shape[0], 1))
    empty_row[2] = 1

    D = np.append(C, empty_row, axis=1)

    return D
