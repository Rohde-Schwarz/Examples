"""
# GitHub examples repository path: RadioTestSets/Python/RsInstrument

This Python example shows how to transfer waveform data (ASCII and binary format)
from CMA180 radio tester to the controller PC. No extra cabling is needed as the CMA180
uses the same port (RFCOM) for both generator and analyzer.

Preconditions:
- Installed RsInstrument Python module from pypi.org
- Installed VISA e.g. R&S Visa 5.12.x or newer

Tested with:
- CMA180, FW: v1.7.20
- Python 3.9
- RsInstrument 1.53.0

Author: R&S Customer Support / PJ
Updated on 19.10.2022
Version: v1.0

Technical support -> https://www.rohde-schwarz.com/support

Before running, please always check this script for unsuitable setting !
This example does not claim to be complete. All information have been
compiled with care. However, errors can’t be ruled out.

"""

# --> Import necessary packets  
from RsInstrument import *  # The RsInstrument package is hosted on pypi.org, see Readme.txt for more details
import matplotlib.pyplot as plt
from time import sleep
from time import time

# Predefine variables
resource = 'TCPIP0::10.205.3.209::INSTR'  # VISA resource string for the device


RsInstrument.assert_minimum_version('1.53.0')  # Ensure to use a dedicated minimum version of RsInstrument
# Define the device handle
# cma180 = RsInstrument(resource)
cma180 = RsInstrument(resource, False, False, "SelectVisa='rs'")


def comprep():
    """Preparation of the communication (termination, etc...)"""
    print(f'VISA Manufacturer: {cma180.visa_manufacturer}')  # Confirm VISA package to be chosen
    cma180.visa_timeout = 5000  # Timeout for VISA Read Operations
    cma180.opc_timeout = 5000  # Timeout for opc-synchronised operations
    cma180.instrument_status_checking = True  # Error check after each command, can be True or False
    cma180.clear_status()  # Clear status register
    cma180.logger.log_to_console = False  # Route SCPI logging feature to console on (True) or off (False)
    cma180.logger.mode = LoggingMode.Off  # Switch On or Off SCPI logging
    cma180.write_str_with_opc('SYSTem:DISPlay:UPDate ON')  # Activate CMA display whilst remote control


def close():
    """Close the VISA session"""
    cma180.close()


def comcheck():
    """Check communication with the device"""
    # Just knock on the door to see if instrument is present
    idn_response = cma180.query_str('*IDN?')
    sleep(1)
    print('Hello, I am ' + idn_response)


def measprep():
    """Switch CMA to analog SA mode and feed in a CW signal over RFCOM"""
    # Define analyzer parameters
    cma180.write_with_opc('CONFigure:BASE:SCENario SPECtrum')
    cma180.write_with_opc('CONFigure:GPRF:MEASurement1:SPECtrum:FREQuency:CENTer 433 MHz')
    cma180.write_with_opc('CONFigure:GPRF:MEASurement1:SPECtrum:FREQuency:SPAN 10 MHz')
    cma180.write_with_opc('CONFigure:AFRF:MEASurement1:RFSettings:CONNector RFCom')

    # Define generator parameters
    cma180.write_with_opc('SOURce:AFRF:GENerator1:RFSettings:CONNector RFCOM')
    cma180.write_with_opc('SOURce:AFRF:GENerator1:RFSettings:FREQuency 433 MHz')
    cma180.write_with_opc('SOURce:AFRF:GENerator1:RFSettings:LEVel -30 dBm')
    cma180.write_with_opc('SOURce:AFRF:GENerator1:MSCHeme CW')


def meas():
    """Activate generator, perform measurement, get and display measurement on local PC"""
    cma180.write_with_opc('SOURce:AFRF:GENerator1:STATe ON')

    # Perform readout in ASCII mode
    start = time()
    cma180.write_str("FORM:DATA ASC")
    cma180.data_chunk_size = 100000  # Transfer in blocks of 100k bytes (default)
    # Fetch magnitude data
    mag_data_asc = cma180.query_bin_or_ascii_float_list("FETCh:GPRF:MEASurement1:SPECtrum:MAXimum:MAXimum?")
    del mag_data_asc[0]  # Delete first value as it always will be 0
    # Fetch adequate frequency data
    freq_data_asc = cma180.query_bin_or_ascii_float_list("FETCh:GPRF:MEASurement1:SPECtrum:FSWeep:XVALues?")
    del freq_data_asc[0]  # Delete first value as it always will be 0
    print(f'ASCII waveform transfer elapsed time: {time() - start:.3f}sec')
    plt.figure(1)
    plt.plot(freq_data_asc, mag_data_asc)
    plt.title('ASCII waveform')
    plt.show()

    cma180.write_with_opc('SOURce:AFRF:GENerator1:STATe OFF')


#
# ---------------------------
#  Main Program begins here
#  just calling the functions
# ---------------------------
#
    
comprep()
comcheck()
measprep()
meas()
close()


print("I'm done")
