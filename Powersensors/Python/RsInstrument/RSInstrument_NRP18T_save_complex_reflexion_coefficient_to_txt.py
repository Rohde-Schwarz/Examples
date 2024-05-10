"""
# GitHub examples repository path: not known yet

This Python example shows how extract the complex reflection coefficient data from an NRP power sensor to a TXT file.
It is based on the frequency information of the calibration data stored to the sensor.
The needed frequency data can be saved using the S-Parameter Update Multi tool form the NRP toolkit package:
- Start the S-Parameter Update Multi tool
- Sensor / Load Calibration Data
- Choose your sensor and click the "Upload" button followed by "OK"
- Options / Show Cal. Data
- Scroll down to "Absolute Calibration Data"
- Mark all the lines containing frequency information in this section
- Copy it with <CTRL>-C
- Open a file explorer and generate a folder called "tempdata" in drive C:
- Generate a new text document called "frq_list.txt" and paste the data using <CTRL>-P
- Save the text file

Preconditions:
- Installed RsInstrument Python module from pypi.org
- Installed VISA e.g. R&S Visa 5.12.x or newer

Tested with:
- NRP18T, FW v02.50.23042601
- Python 3.12
- RsInstrument 1.70.0

Author: R&S Product Management AE 1GP3 / PJ
Updated on 10.05.2024
Version: v1.0

Technical support -> https://www.rohde-schwarz.com/support

Before running, please always check your setup!
This example does not claim to be complete. All information have been
compiled with care. However, errors can’t be ruled out.

"""

# RsInstrument package is hosted on pypi.org
from RsInstrument import *


# Define variables now
freq_source_file_path = r'C:\tempdata\frq_list.txt'  # Path and filename for the frequency source information
result_file_path = r'C:\tempdata\compdata.txt'  # Path and filename for the frequency source information
visa_resource_name = 'USB::0x0AAD::0x0151::101211::INSTR'


# Define the device handle
nrpt = RsInstrument(visa_resource_name, reset=True)
RsInstrument.assert_minimum_version('1.70.0')


def com_prep():
    """Preparation of the communication (initialization, termination, etc...)"""
    print(f'Hello - I am {nrpt.query('*IDN?')}')
    print(f'And I have the following licences installed: {nrpt.query('*OPT?')}')
    print(f'\nVISA Manufacturer: {nrpt.visa_manufacturer}\n')  # Confirm VISA package to be chosen
    nrpt.visa_timeout = 5000  # Timeout for VISA Read Operations
    nrpt.opc_timeout = 5000  # Timeout for opc-synchronised operations
    nrpt.instrument_status_checking = True  # Error check after each command, can be True or False
    nrpt.clear_status()  # Clear status register
    nrpt.logger.log_to_console = False  # Route SCPI logging feature to console on (True) or off (False)
    nrpt.logger.mode = LoggingMode.Off  # Switch On or Off SCPI logging


def load_freq_list():
    """Gather all the frequency information from the source file into a list"""
    print('Begin to read frequency list...')
    with open(freq_source_file_path) as file:
        freq_list = []
        while line := file.readline():
            freq_list.append(line[:11])
    print(f'Gathered {len(freq_list)} lines containing frequency information\n')
    return freq_list


def write_complex_data():
    """Request Complex Reflection Coefficient data from the sensor and write it into the target file"""
    print('Begin to write the file with complex reflection coefficient data...')
    file = open(result_file_path, 'w')
    file.write('Frequency (Hz);Magnitude;Phase(degrees)\n')
    for value in freq_data:
        nrpt.write(f'SENSe1:FREQuency {value}')
        nrpt.query_opc()
        file.write(value)
        file.write(';')
        file.write(nrpt.query('SENSe1:IGAMma:MAGNitude?'))
        file.write(';')
        file.write(nrpt.query('SENSe1:IGAMma:PHASe?'))
        file.write('\n')
    file.close()
    print(f'All the data has been written to {result_file_path}.\n'
          f'Session will be closed now.')


def close():
    """Close the session"""
    nrpt.close()


# Main program begins here
com_prep()
freq_data = load_freq_list()
write_complex_data()
close()
