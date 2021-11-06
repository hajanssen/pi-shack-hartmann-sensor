import numpy as np
from PIL import Image
from skimage import measure, feature, segmentation, color, morphology

def getSeperation(img_ori,invert=False):
    # load images as grayscale

    if invert == True:
        img_ori = img_ori*-1 +np.max(img_ori)
    
    # Edge detection
    img_can = feature.canny(img_ori**1.2,4,low_threshold=10, high_threshold=30)
    
    #img_open = morphology.closing(img_can,img_disk)
    img_open = morphology.dilation(img_can,morphology.disk(3))
    
    # Element seperation
    segments = segmentation.watershed(img_open)
    
    # labeling of elements (maybe unnecessary)
    label = measure.label(segments)
    # expension doesn't work, i guess 
    sections = segmentation.expand_labels(label, distance=30)

    return sections#, img_ori

def getMomentum(img,img_ori):
    centroid = []
    x = np.zeros(np.max(img)-1)
    y = np.zeros(np.max(img)-1)
    for i in range(2,np.max(img)+1):
        mask = img == i
        M = measure.moments(img_ori * mask)
        x[i-2] = M[0, 1] / M[0, 0]
        y[i-2] = M[1, 0] / M[0, 0]
        
        # fig,ax = plt.subplots(figsize=(4,4))
        # ax.imshow(img_ori * mask, interpolation='none')
        # ax.plot(x[i-1],y[i-1],"or")
    return x, y
