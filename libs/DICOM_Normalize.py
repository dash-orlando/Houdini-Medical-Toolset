# This code is called when instances of this SOP cook.
node = hou.pwd()
geo = node.geometry()

#get min and max values
max = geo.floatAttribValue("MaximumDensity")
min = geo.floatAttribValue("MinimumDensity")

volume = geo.prims()[0]

resolution = volume.resolution()

xRange = range( 0, resolution[0] )
yRange = range( 0, resolution[1] )
zRange = range( 0, resolution[2] )

normal = geo.intAttribValue('Normalized')

if( normal == 1 ):
    raise Exception("Dicom is already normalized, this node is not necesary")

for x in xRange:
    for y in yRange:
        for z in zRange:
            current = volume.voxel( (x, y, z) )
            new = (current - min)/(max - min)
            volume.setVoxel( (x, y, z), new )

geo.setGlobalAttribValue('Normalized', 1)
