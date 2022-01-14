import numpy as np
import matplotlib.pyplot as plt
from scipy import linalg
import time 



# set random seed to scramble the gradient locatoins
start_1 = time.perf_counter()

np.random.seed(0)

# define example data 
k = 20 # nuber gradient points'
xk_amp = np.linspace(0,2*np.pi,k+1) #+ np.random.rand(k+1) /4
yk_amp = np.linspace(0,2*np.pi,k+1) #+ np.random.rand(k+1) /4

# slice pos for gradint
xk_array = xk_amp[0:-1] + (xk_amp[1::] - xk_amp[0:-1])/2
yk_array = yk_amp[0:-1] + (yk_amp[1::] - yk_amp[0:-1])/2

G2x, G2y = np.meshgrid(xk_amp,yk_amp)

Gy_fun = lambda x: np.sin(x) #+ (x**2)/50
G_amp = Gy_fun(G2x) *  Gy_fun(G2y)


G_grad_x = np.diff(G_amp,axis=1)[1::,:]
G_grad_y = np.diff(G_amp,axis=0)[:,1::]

# -----------------------------

# xk yk : gradient position
# G : gradient Manitude

pinv = np.linalg.pinv

#pinv = linalg.pinv
# number of neighbouring points
P = 10

#1 construct vector Gvia Eq. (2)
G = np.concatenate([make1D(G_grad_x),make1D(G_grad_y)]) # append dy to dx like eqasion 2

#2 choose desired shape data locations [Xn,Yn]

n_res = 25
Xn_array = np.linspace(xk_array[0],xk_array[-1],n_res)
Yn_array = np.linspace(yk_array[0],yk_array[-1],n_res) 

Xn_2D, Yn_2D =  np.meshgrid(Xn_array,Yn_array)
Xn, Yn = make1D(Xn_2D), make1D(Yn_2D)

xk_array_1d, yk_array_1d =  np.meshgrid(xk_array,yk_array)
xk_array_1d, yk_array_1d = make1D(xk_array_1d), make1D(yk_array_1d)

# index where the Y array starts 
K = len(xk_array_1d)

# 
C = np.zeros((2*K, len(Xn)))
#C = np.empty((2*K, len(Xn)))
#C[:,:] = np.NaN
time2 = time.perf_counter()
print("building test data time:", (time2 - start_1) *1000 )

#loop over all koordinates [1:100]
for i, (xk ,yk) in enumerate(zip(xk_array_1d, yk_array_1d)):
    # C = np.zeros((2*K, len(Xn)))
    # calculate distance to dots
    dX =  xk - Xn
    dY =  yk - Yn
    
    distance = np.sqrt(np.square(dX) + np.square(dY))
    distance_idx = np.argsort(distance)
    
    dX = Xn[distance_idx[0:P]] - xk
    dY = Yn[distance_idx[0:P]] - yk

    # --- X Components ---
    # taylor series Matrix
    M = np.array([np.ones(len(dX)), 
                  dX,
                  dY,#])
                  (dX**2)/2, 
                  dX*dY,
                  (dX**2)/2])

    # "Zero" Array with the number of Taylor polinom
    V = np.zeros((np.size(M,0),1))
    V[1] = 1

    M_inv = pinv(M)
    C[i,distance_idx[0:P]] = (M_inv@ V).T
    

    # "Zero" Array with the number of Taylor polinom
    V = np.zeros((np.size(M,0),1))
    V[2] = 1
    C[i+K,distance_idx[0:P]] = (M_inv @ V).T


time3 = time.perf_counter()

print("loop duration:", (time3 - time2)  *1000)


empty_row = np.zeros((C.shape[0],1))
empty_row[2] = 1
D = np.append(C, empty_row, axis=1)

Z = pinv(D) @ G

print("last inverse:", (time.perf_counter() - time3)  *1000)
fig, ax = plt.subplots(1,2,figsize=(5,5),dpi=200)
Z_shape = -1*np.reshape(Z[0:-1],(n_res,n_res))
a = ax[0].imshow(G_amp); #plt.colorbar(a)
a = ax[1].imshow(Z_shape); #plt.colorbar(a)
fig.savefig("test.png")


