"""
# GitHub examples repository path: SpectrumAnalyzers/Python/RsInstrument

Created on 2022/04

Author: Jahns_P
Version Number: 1
Date of last change: 2022/04/19
Requires: FSH series SPA, FW 3.30 or newer and adequate options
- Installed RsInstrument Python module from pypi.org
- Installed VISA e.g. R&S Visa 5.12.x or newer

Description: Setup measurement, get trace data, slice it, calculate frequency list, and save data to a local CSV file


General Information:

Please always check this example script for unsuitable setting that may
destroy your DUT before connecting it to the instrument!
This example does not claim to be complete. All information has been
compiled with care. However, errors can not be ruled out.

Please find more information about RsInstrument at
https://rsinstrument.readthedocs.io/en/latest/
"""

from RsInstrument import *
from time import sleep

# Define variables
resource = 'TCPIP::10.205.0.41::INSTR'  # VISA resource string for the device
# resource = 'TCPIP::172.16.10.10::INSTR'  # Original resource string when using USB connection
recdur = 10  # Time in seconds to find max hold peaks
inst_filename = '"\Public\Screen Shots\screenshot.png"'
pc_filename = r'C:\test\FSH_ScreenShot.PNG'


# Define the device handle
instrument = RsInstrument(resource, reset=True, id_query=True, options="SelectVisa='rs'")
'''
- option SelectVisa:
    - 'SelectVisa = 'socket' - uses no VISA implementation for socket connections 
                             - you do not need any VISA-C installation
    - 'SelectVisa = 'rs' - forces usage of Rohde&Schwarz Visa
    - 'SelectVisa = 'ni' - forces usage of National Instruments Visa     
'''


#
# Define subroutines
#


def com_prep():
    """Preparation of the communication (termination, timeout, etc...)"""
    
    print(f'VISA Manufacturer: {instrument.visa_manufacturer}')  # Confirm VISA package to be chosen
    instrument.visa_timeout = 5000  # Timeout in ms for VISA Read Operations
    instrument.opc_timeout = 3000  # Timeout in ms for opc-synchronised operations
    instrument.instrument_status_checking = True  # Error check after each command
    instrument.clear_status()  # Clear status register
  
    
def close():
    """Close the VISA session"""
    instrument.close()


def com_check():
    """Check communication with the device by requesting it's ID"""
    idn_response = instrument.query_str('*IDN?')
    print('Hello, I am ' + idn_response)
    
   
def meas_prep():
    """Prepare instrument for desired measurements
    In this case
    - Set Center Frequency to 1540 MHz
    - Set Span to 100 MHz
    - Set Trace to Max Hold (and Positive Peak automatically)
    """

    instrument.write_str_with_opc('FREQuency:CENTer 2450e6')  # Center Frequency to 2450 MHz
    instrument.write_str_with_opc('FREQuency:SPAN 100e6')  # SPAN is 100 MHz now
    instrument.write_str_with_opc('DISPlay:TRACe1:MODE MAXHold')  # Trace to Max Hold


def measure():
    """Initialize continuous measurement, stop it after the desired time, query trace data"""

    instrument.write_str_with_opc('INITiate:CONTinuous ON')  # Continuous measurement on trace 1 ON
    print('Please wait for maxima to be found...')
    sleep(int(recdur))  # Wait for preset record time
    instrument.write('DISPlay:TRACe1:MODE VIEW')  # Set trace to view mode / stop collecting data
    instrument.query_opc()


def screen_copy():
    """Prepare and perform screenshot, transfer data to local PC"""
    instrument.write('HCOPy:DEVice:LANGuage PNG')  # Select file format for screenshot (possible: PNG or JPG)
    instrument.write(f'MMEMory:NAME {inst_filename}')  # Define path and name for the screenshot on the instrument
    instrument.write('HCOPy:IMMediate')  # Perform screenshot and save it on the analyzer
    # Transfer file to PC
    instrument.data_chunk_size = 10000
    instrument.query_bin_block_to_file(f'MMEMory:DATA? {inst_filename}', f'{pc_filename}', append=False)
    instrument.write(f'MMEMory:DELete {inst_filename}')  # And delete it on the instrument

#
# -------------------------
# Main Program begins here
# -------------------------
#
    

com_prep()
com_check()
meas_prep()
measure()
screen_copy()
close()


print('Program successfully ended.')
print('Wrote trace data into', pc_filename)
