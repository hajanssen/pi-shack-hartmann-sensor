#%%
#%load_ext autoreload
#%autoreload 2
import sys
import numpy as np
sys.path.append("..")
import SHSlib  as sh
import matplotlib.pyplot as plt
#%%

x_pos = np.linspace(10,90,6)
y_pos = np.linspace(10,90,6)

X,Y = np.meshgrid(x_pos,y_pos)

res = (480,640)
res = (480,640)
im_range_x=(0,100)


# Generate Image 
image = sh.simulation.shack(X, Y, res, 
            im_range_x, 
            im_range_x)

image2 = sh.simulation.shack(X-3, Y+3, res, 
            im_range_x, 
            im_range_x)

uint8 = lambda x : ((x/np.max(x) * 255)).astype(np.uint8)

# cast to uint8
img =  uint8(image)
img2 =  uint8(image2)

# %%
# calculate reference
img_lables = sh.analyse.getSeperation(img)
plt.imshow(img_lables)

x_ref,y_ref = sh.analyse.getMomentum(img_lables, img)
plt.plot(x_ref,y_ref,"ro")
plt.show()
# %%

# %%

# %%
