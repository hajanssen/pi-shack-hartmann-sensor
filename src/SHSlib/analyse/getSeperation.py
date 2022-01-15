def getSeperation(img_ori,invert=False):
    import numpy as np
    from skimage import measure, feature, segmentation

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