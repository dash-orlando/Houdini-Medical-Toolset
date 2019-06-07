import hou

node = hou.pwd()
geo = node.geometry()

# get min and max values
max = geo.floatAttribValue("MaximumDensity")
min = geo.floatAttribValue("MinimumDensity")

# get volume information from node
volume = geo.prims()[0]
resolution = volume.resolution()

xRange = range( 0, resolution[0] )
yRange = range( 0, resolution[1] )
zRange = range( 0, resolution[2] )

# check whether the data is already normalized
normal = geo.intAttribValue('Normalized')

# if the data is already normalized, cancel redundant process and prevent data loss
if( normal == 1 ):
    raise Exception("Dicom is already normalized, this node is redundant")

# get current HU value and rescale it between 0 - 1 based on min and max values
for x in xRange:
    for y in yRange:
        for z in zRange:
            current = volume.voxel( (x, y, z) )
            new = (current - min)/(max - min)
            volume.setVoxel( (x, y, z), new )

# tag the geometry as normalized
geo.setGlobalAttribValue('Normalized', 1)
