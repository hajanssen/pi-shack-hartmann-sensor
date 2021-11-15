import numpy as np
from PIL import Image
from skimage import measure, feature, segmentation, color, morphology
import matplotlib.pyplot as plt

def getSeperation(img_ori,invert=False):
    # load images as grayscale

    if invert == True:
        img_ori = img_ori*-1 +np.max(img_ori)
    
    # Edge detection **1.2
    img_can = feature.canny(img_ori**1.2,1,low_threshold=.1, high_threshold=30)
    
    #img_open = morphology.dilation(img_can,morphology.disk(1))
    img_open = img_can

    # Element seperation
    segments = segmentation.watershed(img_open)
    
    # labeling of elements (maybe unnecessary)
    label = measure.label(segments)
    # expension doesn't work, i guess 
    sections = segmentation.expand_labels(label, distance=30)

    return sections#, img_ori

def getMomentum(img,img_ori):
    
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

def getPartner  (img1_x,img1_y,img2_x,img2_y):
    
    # find coresponding points in images, by looking for clooses on s
    partner = []
    for i in range(0,len(img1_x)):
        dis = np.zeros(len(img2_x))

        x_shift = np.array((img1_x[i], img1_y[i]))
        for j in range(0,len(img2_x)):
            v2 = np.array((img2_x[j], img2_y[j]))
            dis[j] = np.linalg.norm(x_shift - v2)
        partner += [np.argmin(dis)]

    x_shift = img2_x[partner] - img1_x
    y_shift = img2_y[partner] - img1_y

    return x_shift, y_shift