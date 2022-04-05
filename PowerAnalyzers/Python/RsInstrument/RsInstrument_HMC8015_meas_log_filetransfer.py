"""
Created on 2020/10
Author: Jahns_P
Version Number: 4
Date of last change: 2022/04/04
Requires: HMC8015, FW 1.403 or newer and adequate options
- Installed RsInstrument Python module 1.20.0 or newer
- Installed VISA e.g. R&S Visa 5.12.x or newer
Description: Setup measurement and log to a file for a certain time, transfer the log file to the PC

General Information:
Please always check this example script for unsuitable setting that may
destroy your DUT before connecting it to the instrument!
This example does not claim to be complete. All information has been
compiled with care. However errors can not be ruled out.
Please find more information about RsInstrument at
https://rsinstrument.readthedocs.io/en/latest/
"""

# --> Import necessary packets
from RsInstrument import *
from time import sleep

RsInstrument.assert_minimum_version('1.20.0')

# Define variables
resource = 'TCPIP::10.205.0.53::5025::SOCKET'  # VISA resource string for the device
x = 1  # For counters
y = 1  # For counters also
intdurtime = "15"  # Integrator duration time in seconds
loopResponse = "1"  # Variable for diverse loop requests
Response = "0"  # Variable for diverse requests
pagenum = 1  # Number of the display page to be logged
logdur = 2  # Log time in seconds
LogFileName = 'LOG1234.CSV'  # Name of the log file
pcFilePath = r'c:\temp\logdata.csv'

# Make sure you have the last version of the RsInstrument
RsInstrument.assert_minimum_version('1.21.0.78')

# Define the device handle
hmc = RsInstrument(resource, True, True, "SelectVisa='rs'")
"""
(resource, True, True, "SelectVisa='rs'") has the following meaning:
(VISA-resource, id_query, reset, options)
- id_query: if True: the instrument's model name is verified against the models 
supported by the driver and eventually throws an exception.   
- reset: Resets the instrument (sends *RST) command and clears its status syb-system
- option SelectVisa:
            'SelectVisa = 'socket' - uses no VISA implementation for socket connections 
                                   - you do not need any VISA-C installation
            'SelectVisa = 'rs' - forces usage of Rohde&Schwarz Visa
            'SelectVisa = 'ni' - forces usage of National Instruments Visa     
"""


# ----------------- Define subroutines for error and command completion requests -----------------
def comprep():
    """Preparation of the communication (termination, etc...)"""
    print(f'VISA Manufacturer: {hmc.visa_manufacturer}')  # Confirm VISA package to be chosen
    hmc.visa_timeout = 5000  # Timeout for VISA Read Operations
    hmc.opc_timeout = 3000  # Timeout for opc-synchronised operations
    hmc.instrument_status_checking = True  # Error check after each command
    hmc.clear_status()  # Clear status register


def close():
    """Close the VISA session"""
    hmc.close()


def comcheck():
    """Check communication with the device"""

    # Just knock on the door to see if instrument is present
    idn_response = hmc.query_str('*IDN?')
    sleep(1)
    print('Hello, I am ' + idn_response)


def measprep():
    """Prepare instrument for desired measurements
    There are four measurement windows with 6 cells each available
    Command is "VIEW:NUMeric:PAGE<n>:CELL<m>:FUNCtion?"
    Where <n> is number of page (1...4)
    and   <m> is number of cell (1...6-10)
    With functions
    P Active power P (Watt)
    S Apparent power S (VA)
    Q Reactive power Q (var)
    LAMBda Power factor λ (PF)
    PHI Phase difference Φ ( ° )
    FU Voltage frequency fU (V)
    FI Current frequency fI (A)
    URMS True rms voltage Urms (V)
    UAVG Voltage average (V)
    IRMS True rms current Irms (A)
    IAVG Current average (A)
    UTHD Total harmonic distortion of voltage Uthd (THD %)
    ITHD Total harmonic distortion of current Ithd (THD %)
    FPLL PLL source frequency fPLL (Hz)
    TIME Integration time
    WH Watt hour (Wh)
    WHP Positive watt hour (Wh)
    WHM Negative watt hour (Wh)
    AH Ampere hour (Ah)
    AHP Positive ampere hour (Ah)
    AHM Negative ampere hour (Ah)
    URANge Voltage range
    IRANge Current range
    EMPTy Empty cell
    """

    hmc.write_str_with_opc('VIEW:NUMeric:PAGE1:CELL1:FUNCtion URMS')  # Page1 Cell1 to root mean square voltage
    hmc.write_str_with_opc('VIEW:NUMeric:PAGE1:CELL2:FUNCtion UAVG')  # Page1 Cell2 to average voltage
    hmc.write_str_with_opc('VIEW:NUMeric:PAGE1:CELL3:FUNCtion IRMS')  # Page1 Cell3 to root mean square current
    hmc.write_str_with_opc('VIEW:NUMeric:PAGE1:CELL4:FUNCtion IAVG')  # Page1 Cell4 to average current
    hmc.write_str_with_opc('VIEW:NUMeric:PAGE1:CELL5:FUNCtion P')  # Page1 Cell5 to active power
    hmc.write_str_with_opc('VIEW:NUMeric:PAGE1:CELL6:FUNCtion S')  # Page1 Cell6 to apparent power


def log():
    """Define and begin logging for all 6 set measurements (on 1st screen).
    Also check the directory if the file exists after logging process is complete."""

    try:  # Delete the logfile (if already existing) and
        hmc.write_str_with_opc(f'DATA:DELETE "{LogFileName}",EXT')  # insert a try block to prevent throwing an
    except StatusException:  # error when the log file to be deleted is
        pass  # not present

    hmc.write_int_with_opc('LOG:PAGE ', pagenum)  # The defined page will be used for logging
    hmc.write_str_with_opc('LOG:MODE DURation')  # Log mode is set to a dedicated time
    hmc.write_int_with_opc('LOG:DURation ', logdur)  # Set dedicated time in seconds for logging duration
    hmc.write_str_with_opc('LOG:INTerval MIN')  # Change the logging interval to minimum (100ms)
    hmc.write_str_with_opc(f'LOG:FNAME "{LogFileName}",EXT')  # Define name and location for the log file
    hmc.write_str_with_opc('LOG:STATe ON')  # Now start logging
    print('\nLogging has started - please wait for', logdur + 1, 'seconds...')
    sleep(int(logdur + 1))  # Wait for the log to be written
    file_response = hmc.query_str('DATA:LIST? EXT')  # Read out directory content
    print('\nThe following files have been found: ' + file_response)


def fileget():
    """Transfer the log file to the local PC"""

    hmc.data_chunk_size = 10000  # Define Chunk size (helps with bigger files)
    append = False
    pc_file_path = r'c:\temp\logdata.csv'
    print('Now transferring the log file...')
    hmc.query_bin_block_to_file(f"DATA:DATA? '{LogFileName}',EXT", pc_file_path,
                                append)  # Directly stream the file to local PC
    print(f'\nFile saved to {pc_file_path}')
    hmc.write_str_with_opc(f'DATA:DELETE "{LogFileName}",EXT')  # Delete the log file after completion


# -------------------------
# Main Program begins here
# -------------------------


comprep()
comcheck()
measprep()
log()
fileget()
close()

print("Program successfully ended.")
