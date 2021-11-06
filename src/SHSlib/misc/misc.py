
#%%
norm = lambda A : A*-1 +np.max(A)


# load images
img_ori = norm(np.array(Image.open("1.png").convert('L')))
img_dis = norm(np.array(Image.open("2.png").convert('L')))

img_can = feature.canny(img_ori,3,low_threshold=0.1, high_threshold=0.1)
segments = segmentation.watershed(img_can)
label = measure.label(segments) # not sure why this is necessary 
sections = segmentation.expand_labels(label, distance=3000)

(fig,ax1) = plt.subplots(figsize=(15,15))
im = plt.imshow(sections, interpolation='none')
plt.colorbar(im)

#%%
centroid = []
for i in range(2,np.max(sections)+1):
    mask = sections == i
    M = measure.moments(img_ori * mask)
    M = (M[1, 0] / M[0, 0], M[0, 1] / M[0, 0])
    centroid += [M]

(fig,ax1) = plt.subplots(figsize=(10,10))
im = ax1.imshow(img_ori * (sections > 1) , interpolation='none')

for c in centroid:
    ax1.plot(c[1],c[0],"ro")

plt.colorbar(im)