# Import Clib if present

from distutils.log import error
import os
import pathlib
import sys 
# from numpy import size
# from sympy import E
curretn_folder = str(pathlib.Path(__file__).parent.resolve())
files = os.listdir(curretn_folder)

# check if system is linux and  
#       if a sheard libray of the lib is in current path
Clib_is_present = False

if sys.platform.startswith('linux') and any(x=="Clib.so" for x in files):
    from ctypes import CDLL, POINTER, c_double
    import ctypes as c
    import numpy as np
    # C-type corresponding to numpy array 
    Clib = CDLL(curretn_folder + "/Clib.so")
    
    ND_POINTER_uint = np.ctypeslib.ndpointer(dtype=np.uintc, 
                                        ndim=1,
                                        flags="C")

    ND_POINTER_double = np.ctypeslib.ndpointer(dtype=np.float64, 
                                        ndim=1,
                                        flags="C")

    Clib.getMomentum.argtypes = [ND_POINTER_uint, c.c_size_t,
                                    ND_POINTER_uint, c.c_size_t,
                                    ND_POINTER_uint, c.c_size_t,
                                    ND_POINTER_uint, c.c_size_t,
                                    ND_POINTER_double, c.c_size_t,
                                    ND_POINTER_double, c.c_size_t]

    Clib.getMomentum.restype = None
    Clib_is_present = True



def getMomentum(img_lables,img_sensor,algorythm="C"):
     
    if algorythm == "C" and Clib_is_present and sys.platform.startswith('linux'):
        #img_lables = img_lables + 1
        x_len = np.shape(img_lables)[0]
        y_len = np.shape(img_lables)[1]

        X = np.arange(x_len)[np.newaxis].T @ np.ones(y_len)[np.newaxis]
        Y = (np.arange(y_len)[np.newaxis].T @ np.ones(x_len)[np.newaxis]).T

        x1 = X**1
        y1 = Y**1

        x1_1d = np.uintc(x1.ravel())
        y1_1d = np.uintc(y1.ravel())

        k = img_lables.max()+1
        Xpos = np.zeros(k)
        Ypos = np.zeros(k)

        
        img_sensor = np.uintc(img_sensor.ravel())
        img_lables = np.uintc(img_lables.ravel())
   
        Clib.getMomentum(img_sensor, img_sensor.size,img_lables, img_lables.size,x1_1d, x1_1d.size,y1_1d, y1_1d.size,Xpos, Xpos.size,Ypos, Ypos.size )
        return Xpos, Ypos
    else:
        algorythm = "CV"

    if algorythm == "CV":
        return getMomentum_CV(img_lables,img_sensor)
    else:
        algorythm = "skimage"

    if algorythm == "skimage":
        return getMomentum_skimage(img_lables,img_sensor)
    else:
        error("no valid algorythm found, install openCV or skimage")
    



def getMomentum_skimage(img,img_ori):

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

def getMomentum_CV(img_lables_in,img_ori):
    from cv2 import moments
    import numpy as np
    img_lables = np.copy(img_lables_in) + 1

    x = np.zeros(np.max(img_lables)-1)
    y = np.zeros(np.max(img_lables)-1)
    
    # [note] this loop could be paralised
    for i in range(2,np.max(img_lables)+1):
        mask = img_lables != i
        img_slice = np.copy(img_ori).astype(np.uint8)
        img_slice[mask] = 0 
    
        M = moments(img_slice)
        x[i-2] = M["m01"] / M["m00"]
        y[i-2] = M["m10"] / M["m00"]

    return y, x
