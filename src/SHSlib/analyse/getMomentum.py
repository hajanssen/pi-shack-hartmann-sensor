#def getMomentum(img,img_ori,algorythm="C_implementation" ):



def getMomentum(img,img_ori):

    import numpy as np
    from skimage import measure

    x = np.zeros(np.max(img)-1)
    y = np.zeros(np.max(img)-1)
    #disk = morphology.disk(10)
    for i in range(2,np.max(img)+1):
        mask = img == i
        #mask = morphology.dilation(mask * 1,disk)
        M = measure.moments(img_ori * mask)
        x[i-2] = M[0, 1] / M[0, 0]
        y[i-2] = M[1, 0] / M[0, 0]
        
    return x, y
