def shack(x_pos, y_pos, res, im_range_x,im_range_y):
    import numpy as np
    from ..simulation import gauss2D 
    from ..simulation import make1D 
 
    # calculate range
    # x_canvis, y_canvis = getRange(x_pos[0,:])
    # ymin, ymax = getRange(y_pos[:,0])
    #print(im_range_x,im_range_y)
    x_array = np.linspace(im_range_x[0],im_range_x[1],res[0])
    y_array = np.linspace(im_range_y[0],im_range_y[1],res[1])
    a = np.zeros((res[0],res[1])) 
    
    x_pos = make1D(x_pos)
    y_pos = make1D(y_pos)

    for i in range(x_pos.shape[0]):
        a += gauss2D(x_array,y_array,x_pos[i],y_pos[i])

    return a
