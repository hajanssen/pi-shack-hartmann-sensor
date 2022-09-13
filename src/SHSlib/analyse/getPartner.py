
def getPartner(img1_center,img2_center):
#def getPartner(img1_x,img1_y,img2_x,img2_y):
    import numpy as np
    
    if isinstance(img1_center, float):
        return np.NaN
    
    img1_x = img1_center[0]
    img1_y = img1_center[1]
    img2_x = img2_center[0]
    img2_y = img2_center[1 ]
    
    # find coresponding points in images, by looking for clooses on s
    partner = []
    for i in range(0,len(img1_x)):
        dis = np.zeros(len(img2_x))

        x_shift = np.array((img1_x[i], img1_y[i]))
        for j in range(0,len(img2_x)):
            v2 = np.array((img2_x[j], img2_y[j]))
            dis[j] = np.linalg.norm(x_shift - v2)
        partner += [np.argmin(dis)]

    dx = img2_x[partner] - img1_x
    dy = img2_y[partner] - img1_y
    
    return (dx, dy)