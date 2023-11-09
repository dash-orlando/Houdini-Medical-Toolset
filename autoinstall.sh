#!/bin/bash

# NOTE: This program expects you to have set up your houdini envirionment.
# It will not work otherwise.

echo ----------------------------------------------------
echo Installing Houdini DICOM Toolset Python Requirements
echo ----------------------------------------------------

# We install the requirements
$HB/hython -m pip install -r requirements.txt

# Done
echo ----------------------------------------------------
echo Installation Completed!
echo ----------------------------------------------------
