"""
# GitHub examples repository path: not known yet
This Python example shows how to install a firmware update for a power sensor via NRX Power Meter.

Preconditions:
- Installed RsInstrument Python module from pypi.org
- Installed VISA e.g. R&S Visa 5.12.x or newer

Tested with:
- NRP18TN, FW v03.20.24090501 / v03.40.25040201
- NRP18E, FW v03.40.25040201
- NRX Power Meter, FW v02.62.24102302
- Python 3.13
- RsInstrument 1.102.0

Author: R&S Product Management AE 1GP3 / KB
Created: 29.07.2025
Version: v1.0

Technical support -> https://www.rohde-schwarz.com/support

Before running, please always check your setup!
This example does not claim to be complete. All information have been
compiled with care. However, errors can’t be ruled out.

"""

from os import path
from time import sleep
from RsInstrument import *

#Variables:
resource = 'TCPIP::NRX-107323.local::hislip0::INSTR'
nrx = RsInstrument(resource, False, True, options="SelectVisa='rs'")
sensorNumber = 1  # Can be 1...4, corresponding to channels A...D
firmware_data = r"C:\tempdata\NRPxSN_03.40.25040201.rsu"  # Absolute path of the file


def com_prep():
    """Set all relevant communication parameters"""
    print(f'\nVISA Manufacturer: {nrx.visa_manufacturer}')
    nrx.visa_timeout = 20000  # Timeout for VISA Read Operations
    nrx.opc_timeout = 20000  # Timeout for opc-synchronised operations
    nrx.instrument_status_checking = True  # Error check after each command, can be True or False
    nrx.clear_status()  # Clear status register
    nrx.logger.log_to_console = False  # Route SCPI logging feature to console on (True) or off (False)
    nrx.logger.mode = LoggingMode.Off


def com_check():
    """Test the device connection, request ID as well as installed options"""
    print('\nHello, I am ' + nrx.query('*IDN?'), end=" ")
    print('and I have the following options available: \n' + nrx.query('*OPT?'))
    print('\n Following Power Sensors are connected: \n' + nrx.query('SENSe0:LIST?'))


def update():
    """Perform the firmware update process"""
    if not path.exists(firmware_data):
         print("Firmware File does not exist")

    with open(firmware_data, "rb") as fh:  # Reading the firmware data as binary data
        content = fh.read()

    # -------------------------------------------------------
    content_size = len(content)
    command = f"SENSe1:SYSTem:FWUPdate #{len(str(content_size))}{content_size}"  # Constructing the command + header
    full_command = command + content.decode('latin-1') + '\n'  # Adding the firmware data as raw string data with
                                                               # termination

    nrx.write(full_command)  # Command to update the power sensor

    # Predefinition of different sensors. Depending on the sensor number, the relevant bit will change.
    ui_mask = 0
    if sensorNumber == 1:
        ui_mask = 2
    if sensorNumber == 2:
        ui_mask = 4
    if sensorNumber == 3:
        ui_mask = 128
    if sensorNumber == 4:
        ui_mask = 256
    while True:
        stat_dev_cond = int(nrx.query("STAT:DEV:COND?"))  # Checking the status of the update
        stat_dev_cond = stat_dev_cond & ui_mask
        if stat_dev_cond == 0:
             break
        else:
            print("Sensor Firmware-Update in progress...")
        sleep(3.0)

    while True:
        stat_dev_cond = int(nrx.query("STAT:DEV:COND?"))  # Checking the status of the sensor reboot
        if stat_dev_cond == 0:
            print('The Sensor is rebooting.')
            sleep(3.0)
        else:
            print('The Update is completed.')
            break


def close():
    """Close the device connection"""
    nrx.write('SYSTem:PRESet')
    nrx.close()


# Main program begins here
com_prep()
com_check()
update()
close()
