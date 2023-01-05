"""

# GitHub examples repository path: Misc/Python/RsInstrument

Created on 2023/01

Author: Customer Support / PJ
Version Number: 1
Date of last change: 2023/01/05
Requires: HMC8012, FW 1.400 or newer and eventually adequate options
- Installed RsInstrument Python module 1.53.0 or newer
- Installed VISA e.g. R&S Visa 5.12.x or newer
- At least define the VISA resource string in line 33 before you start the script

Description: Setup measurement and log to a file for a certain time, transfer the log file to the PC


General Information:

Please always check this example script for unsuitable settings before connecting the instrument!
This example does not claim to be complete. All information has been
compiled with care. However, errors can not be ruled out.

Please find more information about RsInstrument at
https://rsinstrument.readthedocs.io/en/latest/
"""

# --> Import necessary packets  
from RsInstrument import *
from time import sleep


# Define variables
resource = 'TCPIP::10.205.0.218::INSTR'  # VISA resource string for the device
logdur = 5  # Log time in seconds
log_file_name = 'TEST.CSV'  # Name of the HMC log file
pcFilePath = r'c:\Tempdata\logdata.csv'  # Name and Path of the PC log file

# Control the device via RsVISA
hmc8012 = RsInstrument(resource, reset=True, id_query=True, options="SelectVisa='rs', AddTermCharToWriteBinData = OFF, "
                                                                    "OpcQueryAfterWrite = OFF, "
                                                                    "QueryInstrumentStatus = OFF,"
                                                                    "StbInErrorCheck = OFF,"
                                                                    " DisableOpcQuery = ON, VxiCapable = OFF, "
                                                                    "VisaTimeout = 10000, OpcTimeout = 10000")


def comprep():
    """Preparation of the communication (termination, etc...)"""

    RsInstrument.assert_minimum_version('1.53.0')
    print(f'VISA Manufacturer: {hmc8012.visa_manufacturer}')  # Confirm VISA package to be chosen
    hmc8012.clear_status()  # Clear status register
  
    
def close():
    """Close the VISA session"""
    
    hmc8012.close()


def comcheck():
    """Check communication with the device"""

    idnresponse = hmc8012.query_str('*IDN?')  # Check for instrument to be present
    print('Hello, I am ' + idnresponse + '\n')
    
   
def measprep():
    """Prepare instrument for desired measurement
    In this case setting an adequate DC Voltage range and set ADC rate to maximum"""

    hmc8012.write_str('CONF:VOLT:DC 400mV')  # DC Voltage range to 400mV
    hmc8012.write_str('SENSe:ADCRate FAST')  # ADC rate to Fast mode


def logsetup():
    """Prepare and begin logging, in addition check the directory if the file exists
     after logging process is complete."""

    # Delete the log file (if already existing) and insert a try block to prevent
    # throwing an error when the log file to be deleted is not present
    try:
        fileresponse = hmc8012.query_str('DATA:LIST? INT')  # Read out directory before logging (only for information)
        print('Content of the directory at the start is' + fileresponse)
        hmc8012.write_str_with_opc(f'DATA:DELETE "{log_file_name}",INT')  # Delete the logfile if already present
    except IOError:
        pass

    # hmc8012.query_opc()

    hmc8012.write_str('DATA:LOG:MODE TIME')  # Log mode is set to time mode
    hmc8012.write_str('DATA:LOG:TIME ' + str(logdur))  # Set logging duration time (logdur) in seconds
    hmc8012.write_str('DATA:LOG:INTerval 0')  # Set minimal interval time (0) between the logging steps

    hmc8012.write_str('DATA:LOG:FORMAT CSV')  # CSV is log file format
    hmc8012.write_str('DATA:LOG:FNAME "' + log_file_name + '", INT')  # Define Log file name
    print('Log File Name now is', hmc8012.query('DATA:LOG:FNAME?'))
    hmc8012.query_opc()  # Check for command completion

    hmc8012.write_str_with_opc('DATA:LOG:STATe ON ')  # Activate logging
    print('Logging runs now for ' + str(logdur) + ' seconds - please wait!\n')
    sleep(int(logdur+5))  # Wait for the log to be written and add five seconds for logging to be completed


def fileget():
    """Transfer the log file to the local PC"""
    print('Now transferring the log file...\n')
    hmc8012.visa_timeout = 10000  # Enlarge timeout value for VISA Read Operations
    hmc8012.get_session_handle().read_termination = ""  # Disable to process read termination characters
    logdata = hmc8012.query_str_with_opc(f'DATA:DATA? "{log_file_name}",INT')  # Query data into a string
    file = open(pcFilePath, 'w')  # Open the PC log file in write mode
    file.write(logdata)  # And write this string into the PC log file
    file.close()  # Close the PC log file
    hmc8012.get_session_handle().read_termination = "\n"  # Switch back to process read termination character "\n"
    print(f'File saved to {pcFilePath}')
    hmc8012.write_str_with_opc(f'DATA:DELETE "{log_file_name}",INT')
    hmc8012.visa_timeout = 5000  # Set back to original timeout value for VISA Read Operations


# Main Program begins here

comprep()
comcheck()
measprep()
logsetup()
fileget()
close()


print("Program successfully ended.")
