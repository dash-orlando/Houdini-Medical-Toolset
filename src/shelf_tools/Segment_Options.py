from hou import qt as houqt
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

#Class for GUI development
class SegmentPreset():
    def __init__(self):

        #create global level variables for segmentation tool
        self.nodes = hou.selectedNodes() # currently selected nodes
        self.mainWindow = houqt.createWindow() # Window object
        self.mainWindow.setWindowFlags(Qt.WindowStaysOnTopHint) # keep window on top so it doesn't get coverd by the houdini interface
        self.title = "Pick your segment type"
        self.initUI(self.mainWindow)

    # Build the interface for segmentation
    def initUI(self, m):

        m.setWindowTitle(self.title)

        # Create UI Elements to match layout:
        # +--------------------+------------+
        # |Select Segment Type | Dropdown V |
        # +--------------------+------------+
        # |                    | Submit     |
        # +--------------------+------------+

        main_grid = QGridLayout(m)
        main_label = QLabel("Select Your Segment Type")
        main_grid.addWidget(main_label, 0,0,5)

        self.dropdown = QComboBox()
        self.dropdown.addItems(["Airway",
                                "Bone",
                                "Fat",
                                "Water",
                                "Muscle/Soft Tissue",
                                "WhiteMatter",
                                "GreyMatter",
                                "Blood"])

        main_grid.addWidget(self.dropdown, 0, 1, 3)

        submit = QPushButton("Submit")
        submit.clicked.connect(self.act)

        main_grid.addWidget(submit, 3, 1, 2)
        m.show()

    def act(self):
        #make sure a node is selected before trying to run
        if(len(self.nodes) > 0):
            child = self.nodes[0].createOutputNode("DICOM_RangeSegement",
                                                   "Segment_Out_Bones")
            child.setParms({"useDefault": 1,
                            "segmentType": self.dropdown.currentIndex()})
            child = child.createOutputNode("convertvolume", "Create_geometry")
            child.setDisplayFlag(True)
        else: # if not cancel operation and report an error
            print("Select a node before using tool.")

        self.mainWindow.close()

#start the program
window = SegmentPreset()
