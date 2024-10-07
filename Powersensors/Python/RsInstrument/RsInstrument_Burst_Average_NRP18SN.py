"""
# GitHub examples repository path: not known yet

This Python example shows how to perform Burst Average measurements using the R&S SMBV100B as signal source
in combination with an adequate power sensor.
The script first shows ho to set up the sensor for this measurement and how to handle the measurement in the next step.
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
- R&S NRP18SN, FW v02.50.23032501
- R&S SMBV100B, FW 5.30.047.27
- Python 3.12
- RsInstrument 1.82.1
Author: R&S Product Management AE 1GP3 / PJ
Updated on 04.09.2024
Version: v2.0

Technical support -> https://www.rohde-schwarz.com/support

Before running, please always check your setup!
This example does not claim to be complete. All information have been
compiled with care. However, errors can’t be ruled out.

"""

# --> Import necessary packets
from RsInstrument import *
from datetime import datetime

RsInstrument.assert_minimum_version('1.82.1')

# Define variables
resource = 'TCPIP::nrp18sn-101439::hislip0'  # VISA resource string for the device
takes = 200  # Number of measurements to take in complete
nrp = RsInstrument(resource, False, True, options="SelectVisa='rs'") # Define the device handle


# Define all the subroutines


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
    print('Hello, I am ' + nrp.query('*IDN?'), end=" ")
    print('and I have the following options available: \n' + nrp.query('*OPT?'))


def meas_prep():
    """Prepare the sensor for Burst Average measurements"""
    nrp.write('SENSe:FREQuency 1.0e9')  # Working frequency
    nrp.write('TRIGger:SOURce INTernal')  # Trigger source is the measurement signal
    nrp.write('TRIGger:SLOPe POSitive')  # Trigger reacts on a positive slope
    nrp.write('TRIGger:LEVel:UNIT DBM')  # The sensor answers in W as default unit
    nrp.write('TRIGger:LEVel -20')  # Possible value range is from -40 to +23 dBm
    nrp.write('UNIT:POWer DBM')  # Power result unit is dBm now (would also be W by default)
    nrp.write('INITiate:CONTinuous ON')  # Start continuous acquisition
    nrp.query_opc()  # Request for operation complete. This is just an addon as Rsinstrument checks
    # for status byte after each command.
    # nrp.write('SENSe1:POWer:AVG:APERture 1e-3')  # Aperture settings are not needed for this kind of measurement
    nrp.write("SENSe1:FUNCtion 'POWer:BURSt:AVG'")  # Sensor function is burst average now
    nrp.write('SENSe1:TIMing:EXCLude:STARt 0e0')  # Time frame to exclude from measurement after a burst
    # has been recognized.
    nrp.write('SENSe1:TIMing:EXCLude:STOP 0e0')  # Time frame to exclude from the end of the measurement after the end
    # of a burst has been detected.
    nrp.write('SENSe1:POWer:BURSt:DTOLerance 1e-6')  # Sets the dropout time. The dropout time is a time interval in
    # which the pulse end is only recognized if the signal level no longer exceeds the trigger level.

def measurement():
    """Perform burst measurements in a row"""
    print('Starting measurement...')
    miss = 0  # Variable for missing burst signal
    for x in range(takes):
        burst_len = float (nrp.query('SENSe1:POWer:BURSt:LENGth?'))
        while burst_len == 9.91e37:  # Stay in the loop as long as no burst is
            # recognized. 9.91e37 stays for "nan" (SCPI99) which means that no burst is available to read out.
            miss = 1  # Marker for "burstless time" - different output format (additional line feed) is needed after
            # no burst has been detected
            print('\rNo burst signal available for the moment...', end='', flush=True)
            burst_len = float(nrp.query('SENSe1:POWer:BURSt:LENGth?'))
        now = datetime.now()  # Get current system time
        # Print current measurement result in combination with the burst length (time)
        if miss == 1:
            print(f'\n{now.strftime('%H:%M:%S:%f')[:-2]}, Measurement {x} : '
                  f'{float(nrp.query('FETCh1:SCALar:POWer:BURSt?')):.3f} dBm,'
                  f' Burst length: {burst_len:.6f} s')
        else:
            print(f'{now.strftime('%H:%M:%S:%f')[:-2]}, Measurement {x} : '
                  f'{float(nrp.query('FETCh1:SCALar:POWer:BURSt?')):.3f} dBm,'
                  f' Burst length: {burst_len:.6f} s')
        miss = 0


def close():
    """Close the VISA session"""
    nrp.close()


#  Main program begins here

com_prep()
com_check()
meas_prep()
measurement()
close()

print("Program successfully ended.")
