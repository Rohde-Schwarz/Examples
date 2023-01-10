"""
# GitHub examples repository path: Powersupplies/Python/RsInstrument

Created on 2023/01

Author: Customer Support / PJ
Version Number: 1
Date of last change: 2023/05/03
Requires: R&S NGP series PSU, FW 2.025 or newer
- Installed RsInstrument Python module (see https://rsinstrument.readthedocs.io/en/latest/)
- Installed VISA e.g. R&S Visa 5.12.x or newer

Description: Initiate Instrument, configure CH1 and DIO ports as follows:
DIO8 = VPP / DIO6 = OTP / DIO4 = OPP
Please leave CH1 unconnected for testing OVP case.

General Information:
This example does not claim to be complete. All information has been
compiled with care. However, errors can not be ruled out.
"""

from RsInstrument import *
from time import sleep

volsetlo = 3
volsethi = 12
vollim = 11


# Initialize and request instrument for all sessions via VISA
RsInstrument.assert_minimum_version('1.22.0')
ngp = RsInstrument('TCPIP::10.205.0.48::hislip0', reset=True, id_query=True,
                   options="SelectVisa='rs' , LoggingMode = Off, LoggingToConsole = False")

idn = ngp.query_str('*IDN?')
print(f'\nHello, I am {idn}\n')


def close():
    """Close VISA connection"""
    ngp.write('OUTPut:GENeral:STATe OFF')  # Switch off Main Output
    ngp.close()  # Close the connection finally


def setup():
    """Perform all the trigger and protection settings"""

    # First Step: Channel setup
    ngp.write('INSTrument:SELect OUT1')  # Choose CH1
    ngp.write(f'SOURce:VOLTage:LEVel:IMMediate:AMPLitude {volsetlo}')  # Set voltage level
    ngp.write('SOURce:CURRent:LEVel:IMMediate:AMPLitude 1')  # Set current level

    # Second step: Trigger and DIO setup
    ngp.write('TRIGger:CHANnel:DIO8 CH1')  # Assign DIO port 8 (which is PIN1 at the rear connector) to CH1
    ngp.write('TRIGger:CHANnel:DIO6 CH1')  # Assign DIO port 6 (which is PIN2 at the rear connector) to CH1
    ngp.write('TRIGger:CHANnel:DIO4 CH1')  # Assign DIO port 6 (which is PIN3 at the rear connector) to CH1
    ngp.write('TRIGger:DIRection:DIO8 OUTPut')  # Set trigger direction for DIO port
    ngp.write('TRIGger:DIRection:DIO6 OUTPut')
    ngp.write('TRIGger:DIRection:DIO4 OUTPut')
    ngp.write('TRIGger:CONDition:DIO8 OVP,1')  # Define trigger condition parameter (Over Voltage Protection)
    ngp.write('TRIGger:CONDition:DIO6 OTP,1')  # Define trigger condition parameter (Over Temperature Protection)
    ngp.write('TRIGger:CONDition:DIO4 OPP,1')  # Define trigger condition parameter (Over Power Protection)
    ngp.query_opc()  # Check for command completion

    # Third step: Channel protection setup (OTP does not need to be set separately)
    ngp.write(f'SOURce:VOLTage:PROTection:LEVel {vollim}')  # Define OVP protection level in V
    ngp.write('SOURce:VOLTage:PROTection:STATe 1')  # Switch on OVP state
    ngp.write('SOURce:POWer:PROTection:LEVel 3')  # Define OPP level in W
    ngp.write('SOURce:POWer:PROTection:STATe 1')  # Switch in OPP state
    ngp.query_opc()  # Check for command completion

    # Fourth step: Enable DIO ports
    ngp.write('TRIGger:ENABle:DIO8 ON')  # Enable trigger state for DIO port
    ngp.write('TRIGger:ENABle:DIO6 ON')
    ngp.write('TRIGger:ENABle:DIO4 ON')
    ngp.query_opc()  # Check for command completion


def protcase():
    """Switch on PSU and test OVP to be tripped"""
    ngp.write('INSTrument:SELect 1')  # Choose CH1
    ngp.write('OUTPut:SELect 1')  # Switch on CH1
    ngp.write('OUTPut:GENeral:STATe 1')  # Switch on main output
    print(f'Currently OVP is not tripped. Voltage is set to {volsetlo} V, '
          f'OVP value of {vollim} V has not been reached.')
    print('PIN1 of the DIO connector is still low against PIN5 (digital ground)\n')
    print('...waiting for 10 seconds...\n')
    sleep(10)
    ngp.write(f'SOURce:VOLTage:LEVel:IMMediate:AMPLitude {volsethi}')
    print(f'After setting the output voltage to {volsethi} V, OVP value of {vollim} V is overridden.')
    print('PIN1 of the DIO connector is now high against PIN5 (digital ground)')


setup()
protcase()
close()

print('\n --> I am done now')
