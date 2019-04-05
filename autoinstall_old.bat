cls
ECHO OFF
color 02
:: This program automatically installs the python requirements for the Houdini DICOM Toolset
:: This program must be executed from the terminal, with administrator rights
ECHO ----------------------------------------------------
ECHO Installing Houdini DICOM Toolset Python Requirements
ECHO ----------------------------------------------------
:: This version of the application has a hard-coded Houdini version, needs to be improved...
:: [1] The program copies copies the list of requirements to the houdini-python directory
copy requirements.txt "C:\Program Files\Side Effects Software\Houdini*\python27\requirements.txt"
:: [2] The program navigates to the houdini-python directory
cd C:\Program Files\Side Effects Software\Houdini*\python27
:: [2] The program installs pip
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
:: [3] The program installs the requirements
python -m pip install -r requirements.txt
:: [4] Clean-up
del requirements.txt
cd C:\Users\flobo\Documents\Gits\PD3D\Houdini-DICOM-Toolset
ECHO ----------------------------------------------------
ECHO Installation Completed!
ECHO ----------------------------------------------------

