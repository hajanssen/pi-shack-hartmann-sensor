#%%
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from skimage import measure, feature, segmentation, color
from scipy import integrate

#%%
norm = lambda A : A*-1 +np.max(A)

# load images
img_ori = norm(np.array(Image.open("1.png").convert('L')))
img_dis = norm(np.array(Image.open("2.png").convert('L')))

ax1 = plt.subplot(121)
plt.imshow( img_ori)

ax2 = plt.subplot(122)
plt.imshow( img_dis)

#%% Gradint of data 

def grad_2D(A):
    A = np.gradient(A)
    A = np.abs(A[0])**2 + np.abs(A[1])**2
    return A

img_org_grad = grad_2D(img_ori)
img_dis_cont = measure.find_contours(img_org_grad,70)

(fig,ax1) = plt.subplots(figsize=(10,10))

im1 = ax1.imshow(img_org_grad)
plt.colorbar(im1)

for contour in img_dis_cont:
    ax1.plot(contour[:, 1], contour[:, 0], linewidth=2)

#%%

img_dis_grad = grad_2D(img_dis)

ax2 = plt.subplot(122)
plt.imshow(img_dis_grad)

#%% Contour Plot 
img_dis_cont = measure.find_contours(img_dis_grad,0.8)
ax2 = plt.subplot(122,0.8)
plt.imshow(img_dis_cont)


#%% canny Edge detection 
img = plt.imshow(img_ori)
plt.colorbar(img)
plt.show()

img_can = feature.canny(img_ori,3,low_threshold=0.1, high_threshold=0.1)
(fig,ax1) = plt.subplots(figsize=(15,15))
im = plt.imshow(img_can,interpolation='none')
plt.colorbar(im)
plt.show()

segments = segmentation.watershed(img_can)
label = measure.label(segments) # not sure why this is necessary 
(fig,ax1) = plt.subplots(figsize=(15,15))
im = plt.imshow(label, interpolation='none')
plt.colorbar(im)
plt.show()

sections = segmentation.expand_labels(label, distance=3000)
(fig,ax1) = plt.subplots(figsize=(15,15))
im = plt.imshow(sections, interpolation='none')
plt.colorbar(im)


#%%
color1 = color.label2rgb(sections, image=img_ori,bg_label=10)

#%% direct Blob detection also a possible approche 
doh = feature.blob_doh(img_ori,max_sigma=3, threshold=0.001)

doh