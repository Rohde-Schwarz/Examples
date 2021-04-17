These instrument drivers are a new form of native Python 3.x drivers for Rohde & Schwarz Signal Generators.
This zip file only contains examples of use for the RsSmw Python package. The actual RsSmw package you find here:
https://pypi.org/project/RsSmw/

If you wish to use only the plain SCPI commands, have a look at the RsInstrument package: https://rsinstrument.readthedocs.io/
It contains a generic python VISA interface with all the functionalities you might need for your remote-control tasks.
All the RsInsturment's features are also available in each instrument drivers's utility interface as well.

Preconditions:
- Python 3.6 +
- R&S VISA 5.12 + or any other VISA installation, or no VISA for SocketIO session

Currently supported Signal Generators:
- SMW200A: RsSmw
- SMBV100B: RsSmbv
- SMA100B: RsSmab
- SGT100A: RsSgt

Each package comes with documentation in forms of docstrings optimized for Pycharm.
In the examples, remember to adjust the resourceName string to fit your instrument.

-----------------------------------------------------------------------------------------------------------------------------------------------------

Installation of the package (standard):
Because of the dependency (pyvisa), you need internet connection.

- Open the command prompt (Windows Start, type 'cmd' + Enter)
- Navigate to you Python installation folder (Subfolder 'Scripts', where pip.exe is located) with the 'cd' command. Example:
	cd c:\Users\JohnSmith\AppData\Local\Programs\Python\Python36\Scripts
- Run:
	pip install RsSmw


Offline installation:
- Download and run the RsInstrument offline installer python script: https://cdn.rohde-schwarz.com/pws/service_support/driver_pagedq/files_1/helloworld/rsinstrument_offline_install.py
	This script installs all the dependencies you need for the RsSmw package

- Download the RsSmw package from the pypi.org: https://pypi.org/project/RsSmw/#files
	Example: Your download path is 'c:\temp\RsSmw-4.80.0.25.tar'

- Open the command prompt (Windows Start, type 'cmd' + Enter)
- Navigate to you Python installation folder (Subfolder 'Scripts', where pip.exe is located) with the 'cd' command. Example:
	cd c:\Users\JohnSmith\AppData\Local\Programs\Python\Python36\Scripts
- Run:
	pip install c:\temp\RsSmw-4.80.0.25.tar