"""
# GitHub examples repository path: Oscilloscopes/Python/RsInstrument

Created on 2023/03

Author: Customer Support PJ
Version Number: 1
Date of last change: 2023/03/16
Requires: R&S RTH1002, FW: v1.80.3.4
- Installed RsInstrument Python module (see https://rsinstrument.readthedocs.io/en/latest/)
- Installed VISA e.g. R&S Visa 5.12.x or newer
- Can Bus Signal (CAN_L) connected to CH1 of the instrument
- Eventually change logging path and file name before starting the script

Description: Example of setting up and measuring the CAN bus Low Wire.
             Save the decoded frame data to a .txt file.


General Information:
This example does not claim to be complete. All information has been
compiled with care. However, errors can not be ruled out.

"""
import os

from RsInstrument import *  # The RsInstrument package is hosted on pypi.org, see Readme.txt for more details
from os import path


# Define variables
LogFilePath = r'C:\RTH-Test\Data'
LogFileName = 'data.txt'
Resource = 'TCPIP::10.205.0.11::INSTR'  # VISA identifier of the device

# Initiate Instrument session

RsInstrument.assert_minimum_version("1.53")  # Check for RsInstrument version and stop if version is less than xx
rth = RsInstrument(Resource, reset=True, id_query=False,
                   options="SelectVisa='rs' , LoggingMode = Off, LoggingToConsole = False")
print('\nHello, I am ' + rth.query('*IDN?') + '\n')


def meas_prep():
    """Set instrument to defined mode and operating state"""
    rth.write('OP:MODE YT')  # Start SCOPE mode
    rth.write('AUToscale')  # Perform autoset
    rth.write('Timebase:SCALe 2e-3')  # Set Time Base
    rth.write('BUS:TYPE CAN')  # Set BUS type protocol to CAN
    rth.write('BUS:CAN:DATA:SOURce C1')  # Set BUS source to CH1
    rth.write('BUS:CAN:Type CANL')  # Set CAN type to CAN_L
    rth.write('BUS:FORMat DEC')  # Set Bus format to decimal
    rth.query_opc()
    rth.write('BUS:CAN:BITR 50000')  # Set CAN bit-rate
    rth.write('BUS:CAN:TECHnology USER')  # Set CAN technology to User (finding own Threshold Level)
    rth.write('CHANnel1:THReshold:FINDlevel')  # Find the right threshold level
    rth.write('BUS:FORMat HEX')  # Set BUS decoding to desired format (BIN | OCT | DEC | HEX | ASCii)
    rth.write('BUS:STATE ON')  # Switch on BUS decoding
    rth.write('TRIGger:MODE SINGle')  # Set unit to single trigger mode
    rth.query_opc()

    # A dedicated trigger type can be defined for the CAN bus as well
    # Please refer to the TRIGger:CAN:xxx commands in the RTH manual.
    # After preset, it's defined to react on diverse conditions.


def path_check():
    if not path.isdir(LogFilePath):
        os.makedirs(LogFilePath)
        print('Created destination file path.')

    else:
        print('Destination file path is already present.')


def meas():
    """Initiate and perform the measurement. Results will be directly written into the file."""
    rth.write('RUN')  # Initiate Trigger
    print('Initiated measurement.')
    rth.query_opc()  # Wait for the measurement to be done
    nof = rth.query("BUS:CAN:FCOunt?")  # Get the number of decoded frames
    print(f'Number of decoded frames: {nof}')
    nof = int(nof)

    # Now write the data of all frames into a file (The path must already exist)
    print(f'Write Frame Data into {LogFilePath}\\{LogFileName} now.\n')
    delimiter = '\\'
    log_file_path = LogFilePath + delimiter + LogFileName
    file = open(log_file_path, 'w')  # Open the file for write access
    # Define and write data header row names
    file.write("Frame;")
    file.write("Data;"+chr(10))

    # Start loop to read all the frame data and write it into the file
    x = 0
    while x < nof:
        x = x + 1
        value = str(x)
        f_data = rth.query("BUS:CAN:FRAMe" + value + ":DATA?")
        # There is also some more information available to read out:
        # e.g. frame start, type, ID state/value/type
        file.write(value+";")
        file.write(f_data+";"+chr(10))
    # End of control loop
    # Close the file now and end the job
    file.close()


def close():
    """Close the instrument session"""
    rth.close()


meas_prep()
path_check()
meas()
close()

print('All the data has been saved now.')
