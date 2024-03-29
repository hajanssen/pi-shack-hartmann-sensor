def getSeperation(img, algorythm="CV", min_distance=50):

    if algorythm == "CV":
        return getSeperation_CV(img, min_distance=min_distance)
    if algorythm == "skimage2":
        return getSeperation_skimage2(img, min_distance=min_distance)
    if algorythm == "skimage2":
        return getSeperation_skimage(img, min_distance=min_distance)


def getSeperation_CV(img, min_distance):
    import numpy as np
    from cv2 import distanceTransformWithLabels, DIST_L2
    from skimage.feature import peak_local_max as peak

    # get peak position of spots
    spots = peak(img, min_distance=min_distance)
    # print(spots)
    if 0 > spots.size:
        print("incorrect input to seperation")
        return np.nan

    # reshap peak point in x- and y-array
    x_pos = np.array([x[0] for x in spots])
    y_pos = np.array([x[1] for x in spots])

    # make image with "1" as peak, evrsthin els "0"
    img_mask = np.zeros_like(img, dtype=np.uint8)

    img_mask[x_pos, y_pos] = 1

    n, expanded = distanceTransformWithLabels(np.uint8(img_mask == 0), DIST_L2, 3)
    return expanded


def getSeperation_skimage2(img, min_distance):
    from skimage.measure import label
    from skimage.feature import peak_local_max as peak
    from skimage.segmentation import expand_labels
    import numpy as np

    # get peak position of spots
    spots = peak(img, min_distance=10)

    # reshap peak point in x- and y-array
    x_pos = np.array([x[0] for x in spots])
    y_pos = np.array([x[1] for x in spots])

    # make image with "1" as peak, evrsthin els "0"
    img_mask = np.zeros_like(img)
    img_mask[x_pos, y_pos] = 1

    seg1 = label(img_mask)

    # [note] function uses very slow eucleadian distance implementatoin
    # cv has very fast one
    expanded = expand_labels(seg1, distance=min_distance)
    return expanded


def getSeperation_skimage(img_ori, min_distance, invert=False):
    import numpy as np
    from skimage import measure, feature, segmentation

    # load images as grayscale

    if invert == True:
        img_ori = img_ori * -1 + np.max(img_ori)

    # Edge detection **1.2
    img_can = feature.canny(img_ori**1.2, 1, low_threshold=0.1, high_threshold=30)

    # img_open = morphology.dilation(img_can,morphology.disk(1))
    img_open = img_can

    # Element seperation
    segments = segmentation.watershed(img_open)

    # labeling of elements (maybe unnecessary)
    label = measure.label(segments)
    # expension doesn't work, i guess
    sections = segmentation.expand_labels(label, distance=min_distance)

    return sections  # , img_ori
