#%%
import matplotlib.pyplot as plt
import numpy as np
from simulation import Shak, getRange
from analyses import getSeperation, getMomentum
import importlib
%load_ext autoreload

x_pos = np.linspace(0,100,20)
y_pos = np.linspace(0,100,20)

X,Y = np.meshgrid(x_pos,y_pos)
#%%


# add some curvature, according to polynom  
distortion = np.linspace(-10,10,len(x_pos))[np.newaxis]
dist_X, dist_Y = np.meshgrid(distortion,distortion)
#c = plt.imshow(distortion); plt.colorbar(c); plt.show()

#distortion = (distortion**2 * distortion.T**2)*0.5
#c = plt.imshow(distortion); plt.colorbar(c); plt.show()

#distortion = 10 * (distortion/ np.max(distortion))
#c = plt.imshow(distortion); plt.colorbar(c); plt.show()

# Introduce some randomness 
randomness = 0
Xrn = np.random.rand(X.shape[0], X.shape[1]) * randomness
Yrn = np.random.rand(Y.shape[0], Y.shape[1]) * randomness

Xrn +=  distortion
Yrn +=  distortion.T

resolution = 500
img = Shak(X,Y,resolution,resolution)
imgRn = Shak(X+2,Y+2,resolution,resolution)

to8bit = lambda x : ((255 * x) /np.max(x)).astype(int)

# (fig,ax) = plt.subplots(1,2,figsize=(7,7),dpi=300)
# c = ax[0].imshow(img,cmap='gray',interpolation='nearest'); plt.colorbar(c)
# ax[1].imshow(imgRn,cmap='gray',interpolation='nearest')
# fig .tight_layout()

# (fig,ax) = plt.subplots(1,2,figsize=(7,7),dpi=300)
# c = ax[0].plot(X[0,:],"") #,cmap='gray',interpolation='nearest'); plt.colorbar(c)
# c = ax[1].plot((X+dist_X)[:,1]) #,cmap='gray',interpolation='nearest'); plt.colorbar(c)
# fig.tight_layout()


img_8bit = ((255 * img) /np.max(img)).astype(int)

img_1_ori = to8bit(img)
img_2_ori = to8bit(imgRn)

img_1_sep = getSeperation(img_1_ori, invert=True)
img_2_sep = getSeperation(img_2_ori, invert=True)

img1_x, img1_y = getMomentum(img_1_sep,img_1_ori)
img2_x, img2_y = getMomentum(img_2_sep,img_2_ori)


# (fig,ax) = plt.subplots(1,2,figsize=(7,7),dpi=300)
# ax[0].imshow(I_sep,cmap='gray',interpolation='nearest')
# ax[1].imshow(I_sep_Rn,cmap='gray',interpolation='nearest')
# fig .tight_layout()

partner = []
for i in range(0,len(img1_x)):
    dis = np.zeros(len(img2_x))

    v1 = np.array((img1_x[i], img1_y[i]))
    for j in range(0,len(img2_x)):
        v2 = np.array((img2_x[j], img2_y[j]))
        dis[j] = np.linalg.norm(v1 - v2)
    partner += [np.argmin(dis)]

#print("time of operation" , time.time() - t1 )
fig,ax = plt.subplots(2,2,figsize=(12,12),dpi=300)

ax[0,0].imshow(img_1_ori, interpolation='none')
#ax[0,0].plot(img1_x, img1_y,"or",label='mass center inside section')
ax[0,0].set_title("Referenz Image")
ax[0,0].legend()

ax[0,1].imshow(img_2_ori, interpolation='none')
#ax[0,1].plot(img1_x, img1_y,"ob", label='mCenter ref')
#ax[0,1].plot(img2_x, img2_y,"or", label='mCenter of this')
#ax[0,1].legend()

for i in range(0,len(partner)):
    ax[0,1].plot([img1_x[i],img2_x[partner[i]]], [img1_y[i],img2_y[partner[i]]],"r")
    v1 = [img1_x[i],img2_x[partner[i]]], [img1_y[i],img2_y[partner[i]]]

ax[0,1].set_title("Distordet Image")

ax[1,0].imshow(img_1_sep, interpolation='none')
#ax[1,0].plot(img1_x, img1_y,"or")
#ax[1,0].set_title("ref Seperated")

ax[1,1].imshow(img_2_sep, interpolation='none')
#ax[1,1].plot(img2_x, img2_y,"or")
#ax[1,1].set_title("ref Seperated")
# #%%
# plt.show()
# plt.plot(img1_x)
# plt.plot(img2_x[partner])
# plt.show()
# plt.plot(img1_y)
# plt.plot(img2_y[partner])

v1 = img1_x - img2_x[partner]
v2 = img1_y - img2_y[partner]
# plt.plot(v1)
# plt.plot(v2)
# plt.show()
fig,ax = plt.subplots(figsize=(7,5),dpi=300)
plt.plot(np.linalg.norm(np.array((v1,v2)),axis=0))
plt.show()
# %%
