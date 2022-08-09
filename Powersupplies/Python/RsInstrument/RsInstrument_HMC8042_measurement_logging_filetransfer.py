# GitHub examples repository path: Powersupplies/Python/RsInstrument

"""

Created on 2020/12

Author: Jahns_P
Version Number: 3
Date of last change: 2022/08/09
Requires: HMC804x, FW 1.400 or newer and adequate options
- Installed RsInstrument Python module 1.50 or newer
- Installed VISA e.g. R&S Visa 5.12.x or newer

Description: Setup CH1 and log to a file for a certain time, transfer the log file to the local PC


General Information:

Please always check this example script for unsuitable setting that may
destroy your DUT before connecting it to the instrument!
This example does not claim to be complete. All information has been
compiled with care. However, errors can not be ruled out.

Please find more information about RsInstrument at
https://rsinstrument.readthedocs.io/en/latest/
"""

# --> Import necessary packets  
from RsInstrument.RsInstrument import *
from time import sleep

# Define variables
resource = 'TCPIP::10.205.0.191::5025::SOCKET'  # VISA resource string for the device
x = 1  # For counters
y = 1  # For counters also
logdur = 2  # Log time in seconds
interv = 0.001  # Log interval time in seconds
log_file_name = 'LOG1234.CSV'  # Name of the log file
pcFilePath = r'c:\temp\logdata.csv'


# Define communication
RsInstrument.assert_minimum_version('1.50')  # Check for RsInstrument version and stop if version number is too low
hmcpsu = RsInstrument(resource, reset=True, id_query=False,
                      options="SelectVisa='rs' , LoggingMode = Off, LoggingToConsole = False")


def comprep():
    """Preparation of the communication (termination, etc...)"""
    
    print(f'VISA Manufacturer: {hmcpsu.visa_manufacturer}')  # Confirm VISA package to be chosen
    hmcpsu.visa_timeout = 5000  # Timeout for VISA Read Operations
    hmcpsu.opc_timeout = 3000  # Timeout for opc-synchronised operations
    hmcpsu.instrument_status_checking = True  # Error check after each command
    hmcpsu.clear_status()  # Clear status register
  
    
def close():
    """Close the VISA session"""
    
    hmcpsu.close()


def comcheck():
    """Check communication with the device"""
    
    # Just knock on the door to see if instrument is present
    idn_response = hmcpsu.query_str('*IDN?')
    sleep(1)
    print('Hello, I am ' + idn_response)
    
   
def measprep():
    """Prepare instrument for desired measurement
    In this case setting an adequate DC Voltage range and set ADC-rate to maximum"""

    hmcpsu.write_str('INSTrument:Select 1')  # Select channel 1
    hmcpsu.write_str('VOLTage 3')  # DC Voltage is 3 V
    hmcpsu.write_str('CURRent 1')  # Current set to 1 A
    hmcpsu.write_str('OUTPut:CHANnel:STATe 1')  # Set CH1 to active state
    hmcpsu.write_str('OUTPut:MASTer:STATe 1')  # Set Main output to active state
    hmcpsu.query_opc()
     
    
def logsetup():
    """Define and begin logging for all 6 set measurements (on 1st screen).
    Also check the directory if the file exists after logging process is complete."""

    # noinspection PyBroadException
    try:  # Delete the logfile (if already existing) and
        hmcpsu.write_str_with_opc(f'DATA:DELETE "{log_file_name}",EXT')  # insert a try block to prevent throwing an
    except Exception:  # Error when the log file to be deleted is not present
        pass

    hmcpsu.write('DATA:LOG:FORMat CSV')
    hmcpsu.write('DATA:LOG:MODE TIME')  # Log mode is time (possible: UNLimited / COUNt / TIME)
    hmcpsu.write('DATA:LOG:INTerval '+str(interv))  # Set logging interval time in seconds (Range: 1ms to 3600s)
    hmcpsu.write('DATA:LOG:TIME '+str(logdur))  # Set dedicated time in seconds for logging duration
    hmcpsu.write(f'DATA:LOG:FNAME "{log_file_name}",EXT')  # Define name and location for the log file
    hmcpsu.write('DATA:LOG:CHANnel:STATe ON')
    hmcpsu.write('LOG:STATe ON')  # Now start logging
    sleep(int(logdur+1))  # Wait for the log to be written
    file_response = hmcpsu.query_str('DATA:LIST? EXT')  # Read out directory content
    print('\nFound the following file(s): '+file_response)
    
    
def fileget():
    """Transfer the log file to the local PC"""
    
    hmcpsu.data_chunk_size = 10000  # Define chunk size (helps with bigger files)
    print('\nTransferring the log file...')
    hmcpsu.query_bin_block_to_file(f"DATA:DATA? '{log_file_name}',EXT", pcFilePath, False)  # Transfer file
    print(f'File saved to {pcFilePath}')
    hmcpsu.write(f'DATA:DELETE "{log_file_name}",EXT')  # Delete the log file after completion


# -------------------------
# Main Program begins here
# -------------------------
    
comprep()
comcheck()
measprep()
logsetup()
fileget()
close()


print('\nProgram successfully ended.')
