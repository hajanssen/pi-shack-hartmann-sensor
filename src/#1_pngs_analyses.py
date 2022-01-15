#%%
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from skimage import measure, feature, segmentation, color, morphology
from scipy import integrate  
import time

# costum functions
from analyses import getSeperation, getMomentum
from simulation import Shak 

#%%

img_1 = np.array(Image.open("1.png").convert('L'))
img_2 = np.array(Image.open("2.png").convert('L'))

img_1_sep, img_1_ori = getSeperation(img_1, invert=True)
img_2_sep, img_2_ori = getSeperation(img_2, invert=True)

img1_x, img1_y = getMomentum(img_1_sep, img_1_ori)
img2_x, img2_y = getMomentum(img_2_sep, img_1_ori)

partner = []
for i in range(0,len(img1_x)):
    dis = np.zeros(len(img2_x))

    v1 = np.array((img1_x[i], img1_y[i]))
    for j in range(0,len(img2_x)):
        v2 = np.array((img2_x[j], img2_y[j]))
        dis[j] = np.linalg.norm(v1 - v2)
    partner += [np.argmin(dis)]

#print("time of operation" , time.time() - t1 )
fig,ax = plt.subplots(2,2,figsize=(12,12),dpi=150)

ax[0,0].imshow(img_1_ori, interpolation='none')
ax[0,0].plot(img1_x, img1_y,"or",label='mass center inside section')
ax[0,0].set_title("Referenz Image")
ax[0,0].legend()

ax[0,1].imshow(img_2_ori, interpolation='none')
ax[0,1].plot(img1_x, img1_y,"ob", label='mCenter ref')
ax[0,1].plot(img2_x, img2_y,"or", label='mCenter of this')
ax[0,1].legend()

for i in range(0,len(partner)):
    ax[0,1].plot([img1_x[i],img2_x[partner[i]]], [img1_y[i],img2_y[partner[i]]],"r")
ax[0,1].set_title("Distordet Image")

ax[1,0].imshow(img_1_sep, interpolation='none')
ax[1,0].plot(img1_x, img1_y,"or")
ax[1,0].set_title("ref Seperated")

ax[1,1].imshow(img_2_sep, interpolation='none')
ax[1,1].plot(img2_x, img2_y,"or")
ax[1,1].set_title("ref Seperated")
# #%%

# %%
