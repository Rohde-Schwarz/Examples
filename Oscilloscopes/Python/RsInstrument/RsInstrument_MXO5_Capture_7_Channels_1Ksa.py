# GitHub examples repository path: Oscilloscopes/Python/RsInstrument

"""

Created on 2024/02

Author: Xavier Cheng
Version Number: 1
Date of last change: 2024/02/16
Requires: R&S MXO5 8 channels with FW 2.2 or newer
- Installed RsInstrument Python module (see the attached RsInstrument_PythonModule folder Readme.txt)
- Installed VISA e.g. R&S Visa 5.12.x or newer

Description: Example about how to use capture 7 or N channels simultaneously and save it into a CSV file.
the duration of writing the datas is performed as well via using time function.
Before launching the script, please activate the 7 channels corresponding to the defined number (numChannel=7) of channels and the ip adress.
and make a Single capture by clicking on RunSingle.
Reduce the Record length to 1Ksa as 1st step in order to get a reasonable size of csv file.

General Information:
This example does not claim to be complete. All information has been
compiled with care. However, errors can not be ruled out.
"""

from RsInstrument import *
import time

# FileName of the saved file including 7 channels ' trace.
FileName = 'MultichannelFile_7Channels.csv'
# Number of channels used.
NumChannels = 7

# Instrument remote: please define the IP address of the instrument
resource_string = 'TCPIP::172.23.183.17::HISLIP0::INSTR'
rto = RsInstrument(resource_string)

# This timeout is defined in milliseconds
rto.visa_timeout = 50000

# Measure the duration of saving all datas into the CSV file
t = time.time()

# Related to NumChannel 1 to 8 used, the related number of trace are gathered and written on csv file
rto.write("FORM REAL,32;")
rto.query_opc()

# Creation of the csv file with context manager to prevent the locking in case of an error
with open(FileName, 'w') as fid:
    for i in range(NumChannels):
        waveform = rto.query_bin_or_ascii_float_list(f'CHAN{i + 1}:DATA?')
        fid.write(str(waveform) + '\n\n\n\n')

# Elapsed duration of the saved csv file is determined.
elapsed_2 = time.time() - t

# print the elapsed duration on screen.
print(f'Total Query duration: {elapsed_2:.3f} secs')

# Close the remote session and the csv file object
rto.close()
fid.close()
