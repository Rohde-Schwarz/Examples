"""
# GitHub examples repository path: Powersupplies/Python/RsInstrument

Created on 2022/03

Author: Jahns_P
Version Number: 1
Date of last change: 2022/03/18
Requires: R&S NGP series PSU, FW 2.015 or newer
- Installed RsInstrument Python module (see https://rsinstrument.readthedocs.io/en/latest/)
- Installed VISA e.g. R&S Visa 5.12.x or newer

Description: Initiate Instrument, configure and start ARB curve on CH1


General Information:
This example does not claim to be complete. All information has been
compiled with care. However, errors can not be ruled out.
"""

from RsInstrument import *
from time import sleep

# Initialize and request instrument for all sessions via VISA
RsInstrument.assert_minimum_version('1.53.0')
ngp = RsInstrument('TCPIP::10.205.0.149::hislip0', True, True,  # Init with IDN query and reset
                   "SelectVisa='rs',")  # Control the device via RsVISA

idn = ngp.query_str('*IDN?')
print(f"\nHello, I am '{idn}'")


def close():
    """Close VISA connection"""
    ngp.close()  # Close the connection finally


def arb_setup():
    """Perform all the ARB settings"""
    ngp.write('INSTrument:SELect OUT1')  # Choose CH1
    ngp.write('ARB:BLOC:DATA 5,1,2,1,12,2,2,1,15,1,2,1')  # Define Arb Block
    # (5 V, 1 A, 2 seconds, interpolated
    # (12 V, 2 A, 2 seconds, interpolated...
    ngp.write('ARB:BLOC:REP 1')  # Block is repeated 1 time in sequence
    ngp.write('ARBitrary:SEQuence:REPetitions 3')  # Sequence will be repeated 3 times
    ngp.write('ARBitrary:SEQuence:BEHavior:END OFF')  # Switch off Channel after sequence is done
    ngp.query_opc()  # Check for command completion using *OPC?
    ngp.write('ARBitrary:SEQuence:TRANsfer')  # Transfer Arb sequence into memory
    ngp.query_opc()  # Check for command completion using *OPC?


def arb_start():
    """Start the ARB curve"""
    ngp.write('ARBitrary:STATe ON')  # Arb is active now
    ngp.write('OUTPut:STATe ON')  # CH1 on (is still chosen from former sequence)
    ngp.write('OUTPut:GENeral:STATe ON')  # Master Output ON
    ngp.query_opc()  # Check for command completion


def off():
    """Wait until CH1 changes to OFF state (ARB sequence is done), then switch off Main Output"""
    state = 1
    print('\n')
    print('Waiting for ARB sequence to be completed', end="")
    while state == 1:
        sleep(0.4)
        print('.', end="")
        state = ngp.query_int('OUTPut:STATe?')  # Request CH1 state
    ngp.write('OUTPut:GENeral:STATe OFF')  # Switch off Main Output


arb_setup()
arb_start()
off()
close()

print('\n --> I am done now')
