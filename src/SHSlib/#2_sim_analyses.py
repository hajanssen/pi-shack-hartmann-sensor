#%%
import matplotlib.pyplot as plt
import numpy as np
from simulation import Shak, getRange, gauss, gauss2D
from analyses import getSeperation, getMomentum
import importlib
from skimage import measure, feature, segmentation, color, morphology

#%load_ext autoreload

x_pos = np.linspace(10,90,20)
y_pos = np.linspace(10,90,20)

X,Y = np.meshgrid(x_pos,y_pos)

# Generate Image 
res = (1000,1000)
im_range_x=(0,100)

img =   Shak(X, Y, res, 
            im_range_x, 
            im_range_x)

imgRn = Shak(X, Y**1.001, res, 
            im_range_x, 
            im_range_x)


# Call Algorithm
to8bit = lambda x : ((255 * x) /np.max(x)).astype(int)
img_8bit = ((255 * img) /np.max(img)).astype(int)

img_1_ori = to8bit(img)
img_2_ori = to8bit(imgRn)

img_1_sep = getSeperation(img_1_ori, invert=True)
img_2_sep = getSeperation(img_2_ori, invert=True)

img1_x, img1_y = getMomentum(img_1_sep,img_1_ori)
img2_x, img2_y = getMomentum(img_2_sep,img_2_ori)

# find one dot in the shiftetd image
partner = []
for i in range(0,len(img1_x)):
    dis = np.zeros(len(img2_x))

    x_shift = np.array((img1_x[i], img1_y[i]))
    for j in range(0,len(img2_x)):
        v2 = np.array((img2_x[j], img2_y[j]))
        dis[j] = np.linalg.norm(x_shift - v2)
    partner += [np.argmin(dis)]

#% plot 2D images
fig,ax = plt.subplots(2,2,figsize=(12,12),dpi=300)

ax[0,0].imshow(img_1_ori, interpolation='none')
ax[0,0].set_title("Referenz Image")

ax[0,1].imshow(img_2_ori, interpolation='none')

for i in range(0,len(partner)):
    ax[0,1].plot([img1_x[i],img2_x[partner[i]]], [img1_y[i],img2_y[partner[i]]],"r")
    x_shift = [img1_x[i],img2_x[partner[i]]], [img1_y[i],img2_y[partner[i]]]

ax[0,1].set_title("Distordet Image")

ax[1,0].imshow(img_1_sep, interpolation='none')
#ax[1,1].imshow(img_2_sep, interpolation='none')


clip_1 = (img_1_sep > 1).astype(int) * 255
clip_2 = (img_2_sep > 1).astype(int) * 255

both_imges = np.dstack((clip_1,clip_2,clip_2))
ax[1,1].imshow(both_imges, interpolation='none')


# investigate individual shifts
x_shift = img1_x - img2_x[partner]
y_shift = img1_y - img2_y[partner]

fig,ax = plt.subplots(figsize=(7,5),dpi=300)
shift_distance = np.sqrt(x_shift**2 + y_shift**2)

#%% shift_distance = (im_range_x[1] - im_range_x[0]) x_shift[]
fig,ax = plt.subplots(2,figsize=(12,12),dpi=300)
c = ax[0].imshow(x_shift.reshape((20,20)))
plt.colorbar(c)
c = ax[1].imshow(y_shift.reshape((20,20)))
plt.colorbar(c)
plt.tight_layout()
plt.show()

# %
labels_tied = np.array([0, 1, 0, 2, 0])
segmentation.expand_labels(labels_tied, 1)

# %%
