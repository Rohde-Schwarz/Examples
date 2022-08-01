# GitHub examples repository path: Powersupplies/Python/RsInstrument

"""

Created on 2022/07

Author: Jahns_P
Version Number: 3
Date of last change: 2022/08/01
Requires: HMP4040, FW 2.71 or newer
- Installed RsInstrument Python module (see the attached RsInstrument_PythonModule folder Readme.txt)
- Installed VISA e.g. R&S Visa 5.12.x or newer

Description: Example about setting up the channels and perform measurements of U and I in a loop

General Information:

Please always check this example script for unsuitable setting that may
destroy your DUT before connecting it to the instrument!
This example does not claim to be complete. All information has been
compiled with care. However, errors can not be ruled out.
"""


from RsInstrument import *
from time import sleep


# Define variables
measnum = 8  # Define number of measurements to take
channum = 4  # Define the number of channels to be used


# Initiate Instrument session
resource = 'TCPIP::10.205.0.89::5025::SOCKET'  # Assign Instrument VISA resource string
RsInstrument.assert_minimum_version("1.50")  # Check for RsInstrument version and stop if version is less than xx
hmp = RsInstrument(resource, reset=True, id_query=False,
                   options="SelectVisa='rs' , LoggingMode = Off, LoggingToConsole = False")


def comprep():
    """Preparation of the communication (termination, etc...)"""
    hmp.visa_timeout = 3000  # Timeout for VISA Read Operations
    hmp.opc_timeout = 3000  # Timeout for opc-synchronised operations
    hmp.clear_status()  # Clear status register


def comcheck():
    """Test Instrument connection and read Identification String"""
    idn = hmp.query_str('*IDN?')
    print(f'\nHello, I am: {idn}')  # Identification String
    print(f'Visa manufacturer: {hmp.visa_manufacturer}')
    print(f'Instrument full name: {hmp.full_instrument_model_name}')
    sleep(1)


def close():
    """Preparation of the communication (termination, etc...)"""
    hmp.write_str('OUTP:GEN OFF')
    hmp.close()


def measprep():
    """Setup Instrument for measurement"""
    x = 1  # counter variable
    while x < channum+1:
        hmp.write(f'INST outp{x}')  # Choose CH1
        hmp.write(f'OUTP:SEL{x} ON')  # Activate Channel
        hmp.write(f'VOLT {x*2}')  # Set Output Voltage in Volts
        hmp.write(f'CURR {x*.3}')  # Set Output Current in Amperes
        hmp.query_opc()
        x += 1  # increase counter by one
    hmp.write("OUTP:GEN ON")                     # Enable Main output
    sleep(.5)  # Time for output capacitors to be fully loaded


def measure():
    """Perform measurement in a predefined loop"""
    x = 1  # Counter over all
    y = 1  # Channel counter
    while x < measnum+1:
        hmp.write('INST OUTP' + str(y))
        hmp.write('OUTP:SEL' + str(y))
        hmp.query_opc()
        voltage = hmp.query_str('MEAS:VOLT?')
        print('\nMeasurement ' + str(x) + ' results in:')
        print('Voltage on CH', y, ' is ', voltage, ' Volt')
        current = hmp.query_str("MEAS:CURR?")
        print('Current on CH', y, ' is ', current, 'Ampere')
        x += 1
        y += 1
        if y == channum + 1:
            y = 1
        sleep(1)


def main():
    comprep()
    comcheck()
    measprep()
    measure()
    close()


main()
print('\n\nTook all the measurements, main output is off now, channels remain active.')
