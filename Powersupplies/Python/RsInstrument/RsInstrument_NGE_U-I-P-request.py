"""
# GitHub examples repository path: Powersupplies/Python/RsInstrument

Created on 2022/03

Author: Jahns_P
Version Number: 1
Date of last change: 2022/03/30
Requires: R&S NGE series PSU, FW 1.54 or newer
- Installed RsInstrument Python module (see https://rsinstrument.readthedocs.io/en/latest/)
- Installed VISA e.g. R&S Visa 5.12.x or newer

Description: Initiate Instrument, configure and start voltage and current settings,
             sequentially read out power, current, voltage


General Information:
This example does not claim to be complete. All information has been
compiled with care. However, errors can not be ruled out.
"""

from RsInstrument import *
from time import sleep

# Initialize and request instrument for all sessions via VISA
RsInstrument.assert_minimum_version('1.53.0')
nge = RsInstrument('TCPIP::10.205.0.76::hislip0', True, True,  # Init with IDN query and reset
                   "SelectVisa='rs',")  # Control the device via RsVISA

idn = nge.query_str('*IDN?')
print(f"\nHello, I am '{idn}'")


def close():
    """Close VISA connection"""
    nge.close()  # Close the connection finally


def ui_setup():
    """Perform all the voltage and current settings"""
    nge.write('INSTrument:NSELect 1')  # Choose CH1
    nge.write('SOURce:VOLTage:LEVel:IMMediate:AMPLitude 10.5')  # Set voltage level
    nge.write('SOURce:CURRent:LEVel:IMMediate:AMPLitude 1')  # Set current level
    nge.write('OUTPut:STATe 1')  # Switch CH1 ON
    nge.write('OUTPut:GENeral 1')  # Main output ON
    nge.query_opc()  # Check for command completion using *OPC?
    sleep(.5)  # Let voltage and current set after switching on


def read_out():
    """Start the ARB curve"""
    val = nge.query_str('MEASure:SCALar:POWer?')  # Request current power
    print('Power readout is: ', val, ' Watts.')
    val = nge.query_str('MEASure:SCALar:VOLTage:DC?')  # ...Voltage
    print('Voltage readout is: ', val, ' Volts.')
    val = nge.query_str('MEASure:SCALar:CURRent:DC?')  # ...Current
    print('Current readout is: ', val, ' Amperes.')


ui_setup()
read_out()
close()

print('\n --> I am done now')
