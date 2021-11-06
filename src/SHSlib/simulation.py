import numpy as np
from numba import njit, prange

@njit
def gauss(x,sig,mu):
    a = (1/ np.sqrt(2 * np.pi * sig**2)) * np.exp(-((x - mu)**2) / (2 * sig**2))
    return  a

@njit
def gauss2D(x,y, dx, dy, sx=.5, sy=.5):
    x = gauss(x,sx,dx)
    y = gauss(y,sy,dy)
    
    c = np.zeros((len(x),len(y)))
    
    for i in prange(0,len(x)):
        c[i,:] = x[i] * y
    return c

@njit(parallel=True)
def Shak(x_pos, y_pos, res_x, res_y):
    # calculate range
    xmin, xmax = getRange(x_pos[0,:])
    ymin, ymax = getRange(y_pos[:,0])

    x_array = np.linspace(xmin,xmax,res_x)
    y_array = np.linspace(ymin,ymax,res_y)
    a = np.zeros((res_x,res_y)) 
    
    x_pos = make1D(x_pos)
    y_pos = make1D(y_pos)

    for i in prange(x_pos.shape[0]):
        a += gauss2D(x_array,y_array,x_pos[i],y_pos[i])
    return a

@njit
def make1D(A):
    return np.reshape(A, A.shape[0] * A.shape[1])

@njit
def getRange(A,margin=0.2):
    Amin = np.min(A) - (margin * A[-1] - A[0])
    Amax = np.max(A)+ (margin * A[-1] -A[0])
    return Amin, Amax
    
