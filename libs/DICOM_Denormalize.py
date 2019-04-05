# This code is called when instances of this SOP cook.
node = hou.pwd()
geo = node.geometry()

# get min and max values
max = geo.floatAttribValue("MaximumDensity")
min = geo.floatAttribValue("MinimumDensity")

# Get volume data from primitive
volume = geo.prims()[0]

# Get voxel size of volume
resolution = volume.resolution()

# Create axis to traverse when reading through volume
xRange = range( 0, resolution[0] )
yRange = range( 0, resolution[1] )
zRange = range( 0, resolution[2] )

# Check to make sure that the volume is already normalized
normalized = geo.intAttribValue("Normalized")

# If dicom is not normalized, then cancel node execution
if(normalized == 0):
    raise Exception("DICOM is not tagged as normalizd, attempting to denormalize it will damage the information")

# Scale values from 0 to 1 back to their originally HU values
for x in xRange:
    for y in yRange:
        for z in zRange:
            current = volume.voxel( (x, y, z) )
            new = current * (max - min) + min
            volume.setVoxel( (x, y, z), new )

# Tag the geometry as de normalized
geo.setGlobalAttribValue('Normalized', 0)
