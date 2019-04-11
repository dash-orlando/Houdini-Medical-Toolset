import hou
import numpy as np
import os
import pydicom as dicom
import ctypes

# create main references to houdini graph and geometry
node = hou.pwd()
geo = node.geometry()

# Initialize blank vairables for patient information and scan information
patient = None
data = None

# Initialize blank variables for attributes - allows for easy acessing those variables later.
SliceThicknes = None
PixelSpacing = None
Orientation = None
SliceLocation = None
SliceLocation2 = None
SliceSize = None

# axis values for up axis
X = 0
Y = 1
Z = 2
nX = 3
nY = 4
nZ = 5

# Create global variables for attributes parameters
volScale = None
new_dicom = None

# main build sequence for volume
def main():

    # Read node parameters to use
    importAttributes()

    # Load data to process, whether it's raw DICOM information or a Numpy array of already processed information
    if new_dicom:
        fileLocation = node.evalParm("directory")
        if not os.path.exists(fileLocation): return

        # Load raw DICOM data into memory
        try:
            patient = loadScan(fileLocation)
        except Exception as e:
            print(e)
            raise Exception("Failed to load scan information")


        # Read data from patient information into the attributes of the geometry
        buildAttributes(patient);

        # Process raw DICOM data into a 3D array of HU values
        try:
            data = getPixelsHU(patient)
        except Exception as e:
            print(e)
            raise Exception("Failed to stack pixel_arrays")

        # store processed data in the same dirctory as the folder containing the DICOM stack
        np.save(fileLocation + "/../imageData", data)

    # load 3D array from presaved file (load from cache)
    else:
        fileLocation = node.evalParm("file")
        if not os.path.isfile(fileLocation):  return
        data = np.load(fileLocation).astype(np.float64)

    # create volume to populate with voxel information
    voxels = createVolume(data)

    # populate volume with voxel information
    fillVolume(voxels, data)


# Read Dicom files into an array, and sort them in scan order
def loadScan(path):

    for s in os.listdir(path):
        temp = dicom.read_file(path + "/" + s)
        

    slices = [dicom.read_file(path + "/" + s) for s in os.listdir(path)]
    slices.sort(key = lambda x: int(x.InstanceNumber))

    # determine image thickness so the slices will be placed into the correct physical space later
    try:
        slice_thickness = np.abs(slices[0].ImagePositionPatient[0] - slices[1].ImagePositionPatient[0])
    except:
        slice_thickness = np.abs(slices[0].SliceLocation - slices[1].SliceLocation)

    for s in slices:
        s.SliceThickness = slice_thickness

    return slices

# Convert array of dicom files into 3D array of scan values
def getPixelsHU(patient):
    image = np.stack([s.pixel_array for s in patient])

    image = image.astype(np.int16)

    image[image == -2000] = 0

    intercept = patient[0].RescaleIntercept
    slope = patient[0].RescaleSlope

    if(slope != 1):
        image = slope * image.astype(np.float64)
        image = image.astype(np.int16)

    image += np.int16(intercept)

    return np.array(image, dtype=np.int16).astype(np.float64)

# Read DICOM meta information and store it as attributes on the detail level of the geometry
def buildAttributes(patient):
    for elem in patient[0]:
        print(elem)

    try:
        geo.addAttrib(hou.attribType.Global, 'SliceThickness', patient[0].SliceThickness)
        global SliceThickness
        SliceThickness = patient[0].SliceThickness
    except Exception as e:
        print("Couldn't bind Slice Thickness attribute beacuse " + e)
        print(e)

    try:
        geo.addAttrib(hou.attribType.Global, 'PixelSpacing', patient[0].PixelSpacing)
        global PixelSpacing
        PixelSpacing = patient[0].PixelSpacing
    except Exception as e:
        print("Couldn't bind Pixel Spacing attribute beacuse ")
        print(e)

    try:
        geo.addAttrib(hou.attribType.Global, 'Orientation', patient[0].ImageOrientationPatient)
        global Orientation
        Orientation = patient[0].ImageOrientationPatient
    except Exception as e:
        print("Couldn't bind Orientation attribute beacuse ")
        print(e)

    try:
        geo.addAttrib(hou.attribType.Global, 'SliceASize', patient[0].ImagePositionPatient)
        geo.addAttrib(hou.attribType.Global, 'SliceBSize', patient[1].ImagePositionPatient)
        global SliceLocation
        SliceLocation = patient[0].ImagePositionPatient
        global SliceLocation2
        SliceLocation2 = patient[1].ImagePositionPatient
    except Exception as e:
        print("Couldn't bind patient positions beacuse ")
        print(e)

    try:
        geo.addAttrib(hou.attribType.Global, 'PixelRows', patient[0].Rows)
        geo.addAttrib(hou.attribType.Global, 'PixelColumns', patient[0].Columns)
        global SliceSize
        SliceSize = [ patient[0].Rows, patient[0].Columns ]
    except Exception as e:
        print("Couldn't bind pixel array size beacuse ")
        print(e)

    try:
        geo.addAttrib(hou.attribType.Global, 'Normalized', 0)
    except Exception as e:
        print("Couldn't create Normalized attribute")
        print(e)

# create volume to contain density information with appropriate physical size
# (assuming a default scene scale of 1 meter per unit) and accurate voxel size
def createVolume(data):
        # calculate 3D Size of sacan data
        xSize = SliceSize[0] * PixelSpacing[0] / 100
        ySize = len(data) * SliceThickness / 100
        zSize = SliceSize[1] * PixelSpacing[1] / 100

        #create volume indecies
        xIndex = len(data[0])
        yIndex = len(data)
        zIndex = len(data[0][0])

        box = hou.BoundingBox(0.0, 0.0, 0.0, zSize * volScale, xSize * volScale, ySize * volScale)
        voxels = geo.createVolume( zIndex, xIndex, yIndex, box )

        return voxels

# For each point of information, write data to the corresponding voxel
def fillVolume(volume, data):
    xRange = range( 0, len(data[0]) )
    yRange = range( 0, len(data) )
    zRange = range( 0, len(data[0][0]) )


    for y in yRange:
        for x in xRange:
            for z in zRange:
                volume.setVoxel((z, len(data[0]) - x - 1, y), data[y][x][z])

    # Write min and max density scale to volume data
    try:
        geo.addAttrib( hou.attribType.Global, 'MinimumDensity', volume.volumeMax() )
        geo.addAttrib( hou.attribType.Global, 'MaximumDensity', volume.volumeMin() )
    except Exception as e:
        print("Couldn't bind density scale attributes.")
        print(e)


#this function needs to be updated whenever new parameters are added (or removed)
def importAttributes():
    #reference global variables
    global volScale
    global new_dicom

    #bind attribute to global varaibles
    try:
        volScale = node.evalParm("volumeScale");
    except Exception as e:
        print("Couldn't find attribute volumeScale")
        print(e)

    try:
        new_dicom = node.evalParm("process_directory")
    except Exception as e:
        print("Couldn't find attribute process_directory")
        print(e)

main()
