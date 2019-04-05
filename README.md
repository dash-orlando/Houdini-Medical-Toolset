# Houdini-DICOM-Toolset
A toolset for segmentation using Houdini


## Installation
The **Houdini DICOM Toolset** was developed using **Houdini 17** on a Windows 10 system.
The following instructions will guide you through the installation of the **Houdini DICOM Toolset** on Windows


### Pre-requisites
0.  Install the latest version of [Houdini](https://www.sidefx.com/download/)
    > **NOTE:** The **Houdini DICOM Toolset** was developed using **Houdini 17**
    
    > **IF** You (the user) do not have **administrator previledges** for the system;
    1.  _Change the installtion path from_ `C:\Program Files\...` to `C:\Apps\...` _or any target directory that does not require admin_

### Windows Installation (Manual)
Install the **python libraries** associated with the **Houdini DICOM Toolset**
1.  Open the Windows **command propmt** as **administrator**
2.  Navigate to **Houdini's** python directory;
    ```
    cd C:\Program Files\Side Effects Software\Houdini 17.X.X\python27
    ```
    > **NOTE:** Your version of **Houdini** may be diferrent, hence the "17.X.X"
3.  Install **pip**:
    Proper installation of **pip** requires bootstrap [[1](https://pip.pypa.io/en/stable/installing/)]
    ```
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python get-pip.py
    ```
    > **NOTE:** Some Windows systems my have "curl" pre-installed, others may not.
    
    > **IF** the terminals responds with; `'curl' is not recognized as an internal or external command, operable program or batch           > file.` **AND** pip does not run properly, please follow the instructions [here](https://stackoverflow.com/questions/28736666/curl-not-recognized-as-an-internal-or-external-command-operable-program-or-batc)
4.  Install the following libraries: [[2](https://pydicom.github.io/pydicom/stable/getting_started.html)]
    ```
    python -m pip install -U numpy
    python -m pip install -U pydicom
    ```
    > **NOTE:** Any additional libraries missing will result in a standard python **ImportError: No module named _____**

### Windows Installation (Automated) --BETA--
The _autoinstall.bat_ application automates steps 1-4 of the manual installation (above)
1.  Open the Windows **command propmt** as **administrator**
2.  Navigate to the **repo** directory in your system
    ```
    cd C:\Users\...\Documents\...\PD3D\Houdini-DICOM-Toolset
    ```
3.  Execute application;
    ```
    autoinstall
    ```

## References
1.  [Bootstrap pip installation](https://pip.pypa.io/en/stable/installing/)
2.  [PyDICOM](https://pydicom.github.io/pydicom/stable/getting_started.html)
