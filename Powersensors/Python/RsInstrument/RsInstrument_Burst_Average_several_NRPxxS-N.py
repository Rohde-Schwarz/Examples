"""
# GitHub examples repository path: not known yet

This Python example shows how to perform sequential Burst Average measurements using the R&S SMBV100B as signal source
in combination with more than one adequate power sensors.
The script first shows how to set up the sensor for this measurement and how to handle the measurement in the next step.
It runs fine with the following pulse modulated signal for example:
-> Pulse Period 1 ms, Pulse Width 500 µs, 0 dBm
Feel free to change the settings on the generator as well as in the script.
Another good parameter setup  is
-> Pulse Period 10 ms, Pulse Width 1 ms, 0 dBm
as it shows the sensor is waiting for the next burst before taking a measurement (again).

Preconditions:
- Installed RsInstrument Python module from pypi.org
- Installed VISA e.g. R&S Visa 5.12.x or newer

Tested with:
- NRP18S, FW v02.50.23032501
- SMBV100B, FW v5.30.047.27, BT 5.3
- Python 3.12
- RsInstrument 1.82.1
Author: R&S Product Management AE 1GP3 / PJ
Updated on 01.10.2024
Version: v1.0

Technical support -> https://www.rohde-schwarz.com/support

Before running, please always check your setup!
This example does not claim to be complete. All information have been
compiled with care. However, errors can’t be ruled out.

"""

# --> Import necessary packets
from RsInstrument import *
from time import sleep
from time import time
from datetime import datetime

RsInstrument.assert_minimum_version('1.82.1')

# Define variables
takes = 10  # Number of measurements to take in complete

# Define the device handle
# List all the VISA identifiers in the next line
idents = ['TCPIP::nrp18sn-101439::hislip0', 'TCPIP::nrp18sn-102244::hislip0', 'USB::0x0AAD::0x0138::100657::INSTR',
          'USB::0x0AAD::0x0138::900001::INSTR', 'USB::0x0AAD::0x0138::900101::INSTR', 'TCPIP::NRP33SN-V-900005::hislip0']
nrp = []
for a in range(len(idents)):  # Generate a list with the correct assignment index for the number of sensors
    nrp.append(f'{a}')
for a in range(len(idents)):  # Add each identifier to the list
    nrp[a] = RsInstrument(idents[a], False, True, options="SelectVisa='rs'")


# Define all the subroutines

def com_prep():
    """Preparation of the communication (termination, etc...)"""
    for i in range(len(idents)):  # Perform operation in a loop for each sensor of the list
        print(f'Instrument N°{i} VISA Manufacturer: {nrp[i].visa_manufacturer}')  # Confirm VISA package to be chosen
        nrp[i].visa_timeout = 5000  # Timeout for VISA Read Operations
        nrp[i].opc_timeout = 5000  # Timeout for opc-synchronised operations
        nrp[i].instrument_status_checking = True  # Error check after each command, can be True or False
        nrp[i].clear_status()  # Clear status register
        nrp[i].logger.log_to_console = False  # Route SCPI logging feature to console on (True) or off (False)
        nrp[i].logger.mode = LoggingMode.Off  # Switch On or Off SCPI logging
        print(f'Hello, instrument N°{i} ({nrp[i].query('*IDN?')}) is initialized now\n')


def meas_prep():
    """Prepare the sensor for Burst Average measurements"""
    for i in range(len(idents)):  # Perform operation in a loop for each sensor of the list
        nrp[i].write('SENSe:FREQuency 2.0e9')  # Working frequency
        nrp[i].write('TRIGger:SOURce INTernal')  # Trigger source is the measurement signal
        nrp[i].write('TRIGger:SLOPe POSitive')  # Trigger reacts on a positive slope
        nrp[i].write('TRIGger:LEVel:UNIT DBM')  # The sensor answers in W as default unit
        nrp[i].write('TRIGger:LEVel -20')  # Possible value range is from -40 to +23 dBm
        nrp[i].write('UNIT:POWer DBM')  # Power result unit is dBm now (would also be W by default)
        nrp[i].write('INITiate:CONTinuous ON')  # Start continuous acquisition
        nrp[i].query_opc()  # Request for operation complete. This is just an addon as Rsinstrument checks
        # for status byte after each command.
        #nrp[i].write('SENSe1:POWer:AVG:APERture 1e-2')  # Aperture settings are not needed for this kind of measurement
        nrp[i].write("SENSe1:FUNCtion 'POWer:BURSt:AVG'")  # Sensor function is burst average now
        nrp[i].write('SENSe1:TIMing:EXCLude:STARt 0e0')  # Time frame to exclude from measurement after a burst
        # has been recognized.
        nrp[i].write('SENSe1:TIMing:EXCLude:STOP 0e0')  # Time frame to exclude from the end of the measurement after the end
        # of a burst has been detected.
        nrp[i].write('SENSe1:POWer:BURSt:DTOLerance 1e-9')  # Sets the dropout time. The dropout time is a time interval
        # in which the pulse end is only recognized if the signal level no longer exceeds the trigger level.


def measurement():
    """Perform burst measurements in a row"""
    print('Starting measurement...')
    for x in range(takes):
        start_time = time()
        for i in range(len(idents)):  # Perform operation in a loop for each sensor of the list
            p_len = float(nrp[i].query('SENSe1:POWer:BURSt:LENGth?'))  # Check for recognized burst length
            if p_len != 9.91e37:  # 9.91e37 stays for "nan" (SCPI99) which means that no burst is available to read out.
                now = datetime.now()  # Get current system time
                # Print current measurement result in combination with the burst length (time)
                print(f'Sensor {i}: {now.strftime('%H:%M:%S:%f')[:-2]}, Measurement {x}:'
                      f' {float(nrp[i].query('FETCh1:SCALar:POWer:BURSt?')):.3f} dBm '
                      f'with a length of {p_len*1000:.3f} ms')
            else:
                # Inform the user that no valid pulse / burst has been recognized
                print(f'Sensor {i}: No burst signal available for the moment...')
                sleep(0.000001)
        end_time = time()
        print(f'The request over all sensors took {end_time - start_time:.3f} s now.\n')


def close():
    """Close the VISA session"""
    for i in range(len(idents)):  # Perform operation in a loop for each sensor of the list
        nrp[i].close()


#  Main program begins here

com_prep()
meas_prep()
measurement()
close()

print("Program successfully ended.")
