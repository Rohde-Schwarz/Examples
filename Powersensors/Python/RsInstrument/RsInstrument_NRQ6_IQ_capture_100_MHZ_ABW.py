"""
# GitHub examples repository path: not known yet

This Python example shows how to capture IQ sample files using the R&S NRQ6 as receiver.
The script will perform two captures and in particular record the timing.

Preconditions:
- Installed RsInstrument Python module from pypi.org
- Installed VISA e.g. R&S Visa 7.2.x or newer

Tested with:
- NRQ6, FW V02.40.23032501
- Python 3.12
- RsInstrument 1.60.0

Author: R&S Product Management AE 1GP3 / PJ
Updated on 10.04.2024
Version: v1.0

Technical support -> https://www.rohde-schwarz.com/support

Before running, please always check your setup!
This example does not claim to be complete. All information have been
compiled with care. However, errors can’t be ruled out.

"""

# --> Import necessary packets
from RsInstrument import *
from time import time

# Define variables
resource = 'TCPIP::192.168.2.26::hislip0'  # VISA resource string for the device


# Define the device handle
nrq = RsInstrument(resource, True, True, options="SelectVisa='rs'")


# Define all the subroutines

def com_prep():
    """Preparation of the communication (termination, etc...)"""
    print(f'\nVISA Manufacturer: {nrq.visa_manufacturer}\n')  # Confirm VISA package to be chosen
    nrq.visa_timeout = 3000  # Timeout for VISA Read Operations
    nrq.opc_timeout = 3000  # Timeout for opc-synchronised operations
    nrq.instrument_status_checking = True  # Error check after each command, can be True or False
    nrq.clear_status()  # Clear status register
    nrq.logger.log_to_console = False  # Route SCPI logging feature to console on (True) or off (False)
    nrq.logger.mode = LoggingMode.Off  # Switch On or Off SCPI logging


def com_check():
    """Test the device connection, request ID as well as installed options"""
    print('Hello, I am ' + nrq.query('*IDN?'), end=" ")
    print('and I have the following options available: \n' + nrq.query('*OPT?'))


def meas_prep():
    """Prepare the devise for the measurement"""
    nrq.write('SENSe1:FUNCtion "XTIMe:VOLT:IQ"')  # Change sensor mode to I/Q
    nrq.write('SENSe1:FREQuency:CENTer 2e09')  # Center Frequency to 2 GHz
    nrq.write('SENSE1:BANDwidth:RESolution:TYPE:AUTO:STATe OFF')  # Change bandwidth setting to manual state
    nrq.write('SENSE1:BANDwidth:RESolution:TYPE NORMal')  # Flat filter type
    nrq.write('SENSE1:BANDwidth:RES 1e8''')  # Analysis bandwidth is 100 MHz now
    nrq.write('SENSE1:TRACe:IQ:RLENgth 15e6')  # IQ trace length is 15 million samples now
    nrq.write('')
    print(f'Current setup parameters: \n'
          f'Center Frequency is {nrq.query('SENSe1:FREQuency:CENTer?')} Hz,\n'
          f'Analysis bandwidth is {nrq.query('SENSe1:BANDwidth:RESolution?')} Hz,\n' 
          f'Trace length is {nrq.query('SENSE1:TRACe:IQ:RLENgth?')} Sa,\n'
          f'Sample Rate is {nrq.query('SENSe1:BANDwidth:SRATe:CUV?')} Sa/s,\n')
    nrq.write('FORM:DATA REAL,64')


def measure():
    """Perform measurement and timing calculation, print results"""
    start = time()  # Capture (system) start time
    nrq.write('INITiate:IMMediate')  # Initiates a single trigger measurement
    nrq.visa_timeout = 10000  # Extend Visa timeout to avoid errors
    output = nrq.query_bin_or_ascii_float_list('FETCh1?')  # Get the measurement in binary format
    nrq.visa_timeout = 3000  # Change back timeout to standard value
    inter = time()  # Capture system time after I/Q data has been received
    duration = inter-start  # And calculate process time
    print(f'After {round(duration, 1)} seconds {len(output)} I/Q samples have been recorded.')
    # Perform 2nd take
    nrq.write('INITiate:IMMediate')
    nrq.visa_timeout = 10000
    output = nrq.query_bin_or_ascii_float_list('FETCh1?')
    nrq.visa_timeout = 3000
    end = time()
    duration = end - start
    print(f'After {round(duration, 1)} seconds both records have been taken,'
          f'with the last one {len(output)} I/Q samples have been recorded.')


def close():
    """Close the VISA session"""
    nrq.close()


#  Main program begins here

com_prep()
com_check()
meas_prep()
measure()
close()

print("Program successfully ended.")
