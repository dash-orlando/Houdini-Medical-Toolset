import hou

node = hou.pwd()
geo = node.geometry()

# Get volume information from primitive
volume = geo.prims()[0]
resolution = volume.resolution()


paddedVolume = geo.createVolume(resolution[0] + 2, resolution[1] + 2, resolution[2] + 2, volume.boundingBox())

xRange = range( 0, resolution[0] + 2 )
yRange = range( 0, resolution[1] + 2 )
zRange = range( 0, resolution[2] + 2 )

for x in xRange:
    for y in yRange:
        for z in zRange:
            if(x == 0 or y == 0 or z == 0):
                paddedVolume.setVoxel( (x, y, z), -1 )
                continue
            if(x == resolution[0] + 1 or y == resolution[1] + 1 or z == resolution[2] + 1 ):
                paddedVolume.setVoxel( (x, y, z), -1 )
                continue

            value = volume.voxel( (x - 1, y - 1, z - 1) )
            paddedVolume.setVoxel( (x, y, z), value )


geo.deletePrims([geo.iterPrims()[0]])
