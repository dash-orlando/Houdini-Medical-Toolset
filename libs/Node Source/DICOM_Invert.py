import hou

node = hou.pwd()
geo = node.geometry()

# Get volume information from primitive
volume = geo.prims()[0]
resolution = volume.resolution()

xRange = range( 0, resolution[0] )
yRange = range( 0, resolution[1] )
zRange = range( 0, resolution[2] )

# Invert voxel values from positive to negative and vice versa
for x in xRange:
    for y in yRange:
        for z in zRange:
            # if the dicom is normalized, then values are form 0 - 1 and a
            # 1-value function will effectively inverse the values otherwise,
            # multiplying by -1 will reverse the volume
            if(geo.intAttribValue('Normalized') == 0):
                volume.setVoxel( (x, y, z), -1 * volume.voxel( (x, y, z) ) )
            else:
                value = 1 - volume.voxel( (x, y, z) )
                volume.setVoxel( (x, y, z), value)
