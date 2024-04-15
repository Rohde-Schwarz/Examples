"""
# GitHub examples repository path: not known yet

This Python example shows how to deal with S - parameters. The S2P file must be converted and uploaded to the
sensor using either the "S2P Wizard" or "S-Parameter Update Multi" tools. Both are part of the NRP Toolkit.
The NRP Toolkit can be downloaded from our website, for example at https://www.rohde-schwarz.com/software/nrp-t-tn/.
The script will list the available files and select one for measurements.

Preconditions:
- Installed RsInstrument Python module from pypi.org
- Installed VISA e.g. R&S Visa 7.2.3 or newer

Tested with:
- NRP18T, FW v02.50.23042601
- Python 3.12
- RsInstrument 1.60.0

Author: R&S Product Management AE 1GP3 / PJ
Updated on 12.04.2024
Version: v1.0

Technical support -> https://www.rohde-schwarz.com/support

Before running, please always check your setup!
This example does not claim to be complete. All information have been
compiled with care. However, errors can’t be ruled out.

"""

# --> Import necessary packets
from RsInstrument import *

# Define variables
resource = 'USB::0x0AAD::0x0151::101211::INSTR'  # VISA resource string for the device

# Define the device handle
nrp = RsInstrument(resource, False, True, options="SelectVisa='rs'")


def com_prep():
    """Preparation of the communication (termination, etc...)"""
    print(f'\nVISA Manufacturer: {nrp.visa_manufacturer}\n')  # Confirm VISA package to be chosen
    nrp.visa_timeout = 5000  # Timeout for VISA Read Operations
    nrp.opc_timeout = 5000  # Timeout for opc-synchronised operations
    nrp.instrument_status_checking = True  # Error check after each command, can be True or False
    nrp.clear_status()  # Clear status register
    nrp.logger.log_to_console = False  # Route SCPI logging feature to console on (True) or off (False)
    nrp.logger.mode = LoggingMode.Off  # Switch On or Off SCPI logging


def com_check():
    """Test the device connection, request ID as well as installed options"""
    print(f'Hello, I am {nrp.query('*IDN?')}\n')


def set_s2p():
    """Handle all the S2P parameters"""
    # Request S-parameter device list first
    resp = nrp.query('SENSE1:CORRection:SPDevice1:LIST?')  # Responds all the s2p parameter devices on the sensor
    resp = resp[1:]  # Remove the first character (quotation mark) of the answer
    resp = resp[:-1]  # Remove the last character (quotation mark) of the answer
    resp = resp.split('\n')
    print('Currently the following S-parameter set numbers / devices are available:')
    x = 0
    while x < len(resp):
        print(resp[x])
        x += 1

    # Now activate the first s-parameter set in the list
    par_set = resp[0]  # Choosing the first s-parameter device in the list (starts with 0!)
    nrp.write(f'SENSe1:CORRection:SPDevice1:SELect {par_set[:4]}')  # And select it - Only the four digits are needed.
    print(f'The following S-parameter set has been selected now: "{par_set}"')
    nrp.write('SENSe1:CORRection:SPDevice:STATe ON')  # Activate the correction
    print('The correction is activated now.\n')


def close():
    """Close the VISA session"""
    nrp.close()


#  Main program begins here

com_prep()
com_check()
set_s2p()
close()

print("Program successfully ended.")
