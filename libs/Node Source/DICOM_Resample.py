import hou
import math
import numpy as np

node = hou.pwd()
geo = node.geometry()

# Program key parameters
newSpacing = [1, 1, 1] # TODO: make this into a parameter call
sliceThickness = geo.floatAttribValue('SliceThickness')
pixelSpacing = geo.floatListAttribValue('PixelSpacing')

# Get source volume and its reesolution
source = geo.prims()[0]
resolution = source.resolution()

# Create empty array with the same voxel scale as the volume
image = np.zeros((resolution[0], resolution[1], resolution[2]))

# Iterate through the volume and assign the voxel density to the numpy array
xRange = range( 0, resolution[0] )
yRange = range( 0, resolution[1] )
zRange = range( 0, resolution[2] )
for x in xRange:
    for y in yRange:
        for z in zRange:
            image[x][y][z] = source.voxel( (x, y, z) )

# Calculate converting the new size of the volume after re-representation
pxlSpace = [pixelSpacing[0], pixelSpacing[1]]
spacing = map(float, ([sliceThickness] + pxlSpace) )
spacing = np.array(list(spacing))

resize_factor = spacing / newSpacing
new_real_shape = image.shape * resize_factor
new_shape = np.round(new_real_shape)
real_resize_factor = new_shape / image.shape
new_spacing = spacing / real_resize_factor

image = zoom(image, real_resize_factor)

# Create new volume using the new values that have been created
box = houd.BoundingBox(0.0, 0.0, 0.0, len(image) * newSpacing[0], len(image[0]) * newSpacing[1], len(image[0][0]) * newSpacing[2] )
data = geo.createVolume( len(image), len(image[0]), len(image[0][0]), box )

xRange = range( 0, len(image) )
yRange = range( 0, len(image[0]) )
zRange = range( 0, len(image[0][0]) )
for x in xRange:
    for y in yRange:
        for z in zRange:
            data.setVoxel( (x, y, z), image[x][y][z] )

# Remove initial volume
geo.deletePrims([geo.iterPrims()[0]])
