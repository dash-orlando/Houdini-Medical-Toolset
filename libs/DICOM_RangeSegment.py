import hou

node = hou.pwd()
geo = node.geometry()

# Extract volume information from primitives
volume = geo.prims()[0]
resolution = volume.resolution()

#get min and max values
max = geo.floatAttribValue("MaximumDensity")
min = geo.floatAttribValue("MinimumDensity")

xRange = range( 0, resolution[0] )
yRange = range( 0, resolution[1] )
zRange = range( 0, resolution[2] )

# Evaluate user input for the range of HU values that should remain after segmentation
rangeL = node.evalParm("voxLow")
rangeH = node.evalParm("voxHigh")

voxLow = geo.findGlobalAttrib('voxLow')
voxHigh = geo.findGlobalAttrib('voxHigh')

template = node.evalParm('segmentType')
default = node.evalParm('useDefault')


# default values for default value segmentation, values are:
# Airway, bone, fat, water, muscle, white matter, grey matter, blood
switcher = [ [-3000, 0],
             [300, 1900],
             [-120, 90],
             [-1, 1],
             [20, 40],
             [20, 30],
             [37, 45],
             [13, 75] ]

# if planning to use default value, overwrite the user given values with defaults
if(default):
    rangeL = switcher[template][0]
    rangeH = switcher[template][1]

if(geo.intAttribValue('Normalized') == 1):
     rangeL = (rangeL - min) / (max - min)
     rangeH = (rangeH - min) / (max - min)



# Set values
for x in xRange:
    for y in yRange:
        for z in zRange:
            if( volume.voxel( (x,y,z) ) < rangeL ):
                volume.setVoxel( (x,y,z), 0 )
            if( volume.voxel( (x,y,z) ) > rangeH ):
                volume.setVoxel( (x,y,z), 0 )
