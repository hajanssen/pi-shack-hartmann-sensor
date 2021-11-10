#%%
import matplotlib.pyplot as plt
import numpy as np
from numba import njit, prange

@njit
def gauss(x,sig,mu):
    a = (1/ np.sqrt(2 * np.pi * sig**2)) * np.exp(-((x - mu)**2) / (2 * sig**2))
    return  a

@njit(parallel=True)
def gauss2D(x,y, dx, dy, sx=0.5, sy=0.5):
    x = gauss(x,sx,dx)
    y = gauss(y,sy,dy)
    
    c = np.zeros((len(x),len(y)))
    
    for i in prange(0,len(x)):
        c[i,:] = x[i] * y
    return c

@njit(parallel=True)
def Shak(x_pos, y_pos, res, im_range_x,im_range_y):
    # calculate range
    # x_canvis, y_canvis = getRange(x_pos[0,:])
    # ymin, ymax = getRange(y_pos[:,0])
    print(im_range_x,im_range_y)
    x_array = np.linspace(im_range_x[0],im_range_x[1],res[0])
    y_array = np.linspace(im_range_y[0],im_range_y[1],res[1])
    a = np.zeros((res[0],res[1])) 
    
    x_pos = make1D(x_pos)
    y_pos = make1D(y_pos)

    for i in range(x_pos.shape[0]):
        a += gauss2D(x_array,y_array,x_pos[i],y_pos[i])
        #plt.imshow(b);plt.show()
        #print("idx:", i,"x:", x_pos[i],"y", y_pos[i])

    return a

@njit
def make1D(A):
    return np.reshape(A, A.shape[0] * A.shape[1])

@njit
def getRange(A,margin=0.2):
    Amin = np.min(A) - (margin * A[-1] - A[0])
    Amax = np.max(A)+ (margin * A[-1] -A[0])
    return Amin, Amax
    

# %%
