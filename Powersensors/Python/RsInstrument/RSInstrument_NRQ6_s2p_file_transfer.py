"""
# GitHub examples repository path: not known yet

This Python example shows how to handle s-parameter sets using the R&S NRQ6 frequency selective power sensor.
The script also performs comparison measurements (S-parameter device active or disconnected). Please connect a
signal source with at least -40 dBm for the measurements.

Preconditions:
- Installed RsInstrument Python module from pypi.org
- Installed VISA e.g. R&S Visa 5.12.x or newer

Tested with:
- NRQ6, FW v02.40
- Python 3.12
- RsInstrument 1.70.0

Author: R&S Product Management AE 1GP3 / PJ
Updated on 07.05.2024
Version: v1.0

Technical support -> https://www.rohde-schwarz.com/support

Before running, please always check your setup!
This example does not claim to be complete. All information have been
compiled with care. However, errors can’t be ruled out.

"""

# RsInstrument package is hosted on pypi.org
from RsInstrument import *


# Define variables now
spar_file_path = r'C:\tempdata\sparfile.s2p'  # Path and filename for the s2p file
spar_dev_name = 'SParDevice'  # Name for the S-Parameter Device in the sensor list
spar_num = '1001'  # Reference number for the S-Parameter Device in the sensor list
visa_resource_name = 'TCPIP::nrq6-900034::hislip0'


# Define the device handle
nrq6 = RsInstrument(visa_resource_name, reset=False)
RsInstrument.assert_minimum_version('1.70.0')


def com_prep():
    """Preparation of the communication (initialization, termination, etc...)"""
    print(f'Hello - I am {nrq6.query('*IDN?')}')
    print(f'And I have the following licences installed: {nrq6.query('*OPT?')}')
    print(f'\nVISA Manufacturer: {nrq6.visa_manufacturer}')  # Confirm VISA package to be chosen
    nrq6.visa_timeout = 5000  # Timeout for VISA Read Operations
    nrq6.opc_timeout = 5000  # Timeout for opc-synchronised operations
    nrq6.instrument_status_checking = True  # Error check after each command, can be True or False
    nrq6.clear_status()  # Clear status register
    nrq6.logger.log_to_console = False  # Route SCPI logging feature to console on (True) or off (False)
    nrq6.logger.mode = LoggingMode.Off  # Switch On or Off SCPI logging


def upload_spar():
    nrq6.write(f'SENSe1:CORRection:SPDevice{spar_num}:UNL 1234')  # Sensor must be unlocked before uploading s2p data
    print(f'Unlocked sensor, S-Parameter Device "{spar_dev_name}" will be added now')
    # Transfer the binary data to the sensor
    nrq6.write_bin_block_from_file(
        f"SENSe1:CORRection:SPDevice{spar_num}:DATA ",  # Important: Don't miss the space after the command!
        spar_file_path)
    nrq6.write(f'SENSe1:CORRection:SPDevice{spar_num}:MNEMonic "{spar_dev_name}"')  # Allocate a logical device number


def meas_prep():
    """Prepare measurement by setting parameters"""
    nrq6.write('SENS:FUNC "POW:AVG"')  # Average power measurement
    nrq6.write('SENS:FREQ 1e9')  # Select working frequency
    nrq6.write('SENS:BAND:RES:TYPE:AUTO OFF')  # Auto Bandwidth Filter selection OFF
    nrq6.write('SENS:BAND:RES:TYPE NORMal')  # Set Bandwidth Filter (possible values: FLAT, NORMal, LTE, W3GPp)
    nrq6.write('SENS:BAND:RES 1e6')  # Set the Measurement Bandwidth to 1 MHz
    nrq6.write('SENS:AVER:STAT ON')  # Averaging ON
    nrq6.write('SENS:AVER:COUN:AUTO OFF')  # Auto-Averaging OFF
    nrq6.write('SENS:AVER:COUN 64')  # Average Count 64
    nrq6.write('SENS:POW:AVG:APER 10e-3')  # 10 ms meas window length
    nrq6.write('UNIT:POWer DBM')  # Power unit is dBm now
    nrq6.write('TRIG:SOUR IMMediate')  # Free running trigger


def measure(step):
    """Perform measurement and display power result"""
    unit = nrq6.query('UNIT:POWer?')
    print(f'Measurement result {step} is {nrq6.query_float('FETCH?'):.2f} {unit}\n')


def spar_check(step):
    """Check for S-Parameter Devices being installed on the system"""
    result = nrq6.query_str('SENSe1:CORRection:SPDevice1:LIST?')
    result = result[1:]
    result = result[:-1]
    if result == "":
        result = "None"
    print(f'Available S-Parameter sets {step}: {result}')
    print()


def enable():
    """Activate S-Parameter Device"""
    nrq6.write(f'SENSe1:CORRection:SPDevice1:SELect {spar_num}')
    nrq6.write('SENSe1:CORRection:SPDevice1:STATe 1')


def disable():
    """Deactivate S-Parameter Device"""
    nrq6.write(f'SENSe1:CORRection:SPDevice1:SELect {spar_num}')
    nrq6.write('SENSe1:CORRection:SPDevice1:STATe 0')


def del_spar():
    """Delete the S-Parameter device"""
    print('Now delete S-Parameter Device')
    nrq6.write(f'SENSe1:CORRection:SPDevice:DELete {spar_num}')


def close():
    """Close the session"""
    nrq6.close()


# Main program begins here
com_prep()
spar_check(step='after initialization')
upload_spar()
spar_check(step=f'after uploading')
meas_prep()
enable()
measure(step='with ACTIVE S-Parameter device')
disable()
measure(step="with NO S-Parameter in use")
del_spar()
spar_check(step=f'after deleting "{spar_dev_name}"')
