
Pi_HQ_cam = Sensor(device="pi_hq_cam")

generic_cam = Sensor(resulution=(300,300), 
                    Pixel_size_um=1.5)


#%%
import cv2
import matplotlib.pyplot as plt
import numpy as np
from simulation import Shak, getRange, gauss, gauss2D
from analyses import getSeperation, getMomentum


x_pos = np.linspace(10,90,10)
y_pos = np.linspace(10,90,10)
X,Y = np.meshgrid(x_pos,y_pos)

# Generate Image 
res = (1000,1000)
im_range_x=(0,100)

img =   Shak(X, Y, res, 
            im_range_x, 
            im_range_x)
#%%

params = cv2.SimpleBlobDetector_Params()
params.filterByInertia = False
params.filterByConvexity = False
params.filterByArea = False
params.filterByInertia = False
params.filterByConvexity = False
#params.maxArea = 100000
#params.minInertiaRatio = 0.05
#params.minConvexity = .60
params.minThreshold = 1
params.maxThreshold = 255

detector = cv2.SimpleBlobDetector_create(params)

vis = np.uint8(255*(img/np.max(img)))
vis = np.dstack((vis,vis,vis))
vis = cv2.cvtColor(vis,cv2.COLOR_BGR2GRAY )#COLOR_BGR2GRAY   #COLOR_GRAY2BGR

c =plt.imshow(vis)
plt.colorbar(c)
plt.show()

keypoints = detector.detect(vis)
keypoints
# %%

# %%
