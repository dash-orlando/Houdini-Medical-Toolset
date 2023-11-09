import hou

# grab root directory
obj = hou.node("/obj")

# create a new geometry object
geo = obj.createNode("geo", "Segmentation")

# create import node set for segmentation
child = geo.createNode("DICOM_Import", "Import_Object")
child = child.createOutputNode("DICOM_Normalize", "Value_Display")
child = child.createOutputNode("DICOM_Padding", "Close_DICOM")
