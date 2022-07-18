# -*- coding: utf-8 -*-
"""
Created on 2022/03

Author: Jahns_P
Version Number: 1
Date of last change: 2022/03/23
Requires: R&S NGU series PSU, FW 3.067 or newer
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
RsInstrument.assert_minimum_version('1.25.0')
ngu = RsInstrument('USB0::0x0AAD::0x0197::3639.3763k03-101267::INSTR', reset=True, id_query=True, options="SelectVisa='rs'")  # Control the device via RsVISA

idn = ngu.query_str('*IDN?')
print(f"\nHello, I am '{idn}'")


def close():
    """Close VISA connection"""
    ngu.close()  # Close the connection finally


def arb_setup():
    """Perform all the ARB an d trigger settings"""
    # *** VPM Mode ***
    # ngu.write('ARBitrary:PRIority:MODE VPM')
    # ngu.write('ARB:DATA 5,0.2,-0.2,2,0,12,0.3,-0.3,2,0,15,0.4,-0.4,2,0')  # Define Arb Data
    # (5 V, 0.2 A, -0.2 A, 2 seconds, not interpolated
    # (12 V, 0.3 A, -0.3 A, 2 seconds, not interpolated...

    # *** CPM Mode ***
    ngu.write('ARBitrary:PRIority:MODE CPM')
    ngu.write('ARB:DATA 5,-5,1,2,0,12,-12,2,2,0,15,-15,1,2,0')  # Define Arb Data as
    # (5 V, -5 V, 1 A, 2 seconds, not interpolated
    # (12 V, -12 V, 2A, 2 seconds, not interpolated...

    ngu.write('ARB:REP 2')  # Block is repeated 2 times
    ngu.write('ARBitrary:BEHavior:END OFF')  # Switch off Channel after sequence is done
    ngu.query_opc()  # Check for command completion using *OPC?
    ngu.write('ARBitrary:TRANsfer 1')  # Transfer Arb sequence
    ngu.query_opc()  # Check for command completion using *OPC?


def arb_start():
    """Start the ARB curve"""
    ngu.write('SOURce:VOLTage 5')
    ngu.write('ARBitrary ON')  # Arb is active now
    ngu.query_opc()  # Check for command completion
    ngu.write('OUTPut ON')  # Main output ON


def off():
    """Wait until CH1 changes to OFF state (ARB sequence is done), then switch off Main Output"""
    state = 1
    print('\n')
    print('Waiting for ARB sequence to be completed', end="")
    while state == 1:
        sleep(0.4)
        print('.', end="")
        state = ngu.query_int('OUTPut:STATe?')  # Request CH1 state
    ngu.write('OUTPut:GENeral:STATe OFF')  # Switch off Main Output


def save_setup():
    """Save and reload the ARB file on the instrument"""
    ngu.write('ARBitrary:FNAMe "ARB01.CSV", INT')
    ngu.write('ARBitrary:SAVE')
    ngu.write('ARBitrary:FNAMe "ARB02.CSV", INT')
    ngu.write('ARBitrary:SAVE')
    ngu.write('ARBitrary:FNAMe "ARB01.CSV", INT')
    ngu.write('ARBitrary:LOAD')


arb_setup()
arb_start()
off()
save_setup()
close()

print('\n --> I am done now')
