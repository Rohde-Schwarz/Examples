# -*- coding: utf-8 -*-
"""

Created on 2022/02

Author: Jahns_P
Version Number: 2
Date of last change: 2022/02/16
Requires: R&S HMF25xx, FW 02.301 or newer
- Installed RsInstrument Python module (see https://rsinstrument.readthedocs.io/en/latest/)
- Installed VISA e.g. R&S Visa 5.12.x or newer

Description: Send an ARB waveform to the instrument and provide the ARB signal to the output

General Information:
This example does not claim to be complete. All information has been
compiled with care. However, errors can not be ruled out.
"""

from RsInstrument import *
from time import sleep


RsInstrument.assert_minimum_version('1.19.0.75')
instr = RsInstrument('TCPIP::10.205.0.72::5025::SOCKET', True, True,  # Init with IDN query and reset
                     "SelectVisa='rs',"  # VISA type selection (valid parameters: rs or ni)
                     " Termination Character='\n',"  # Just to show how this is done. \n ist standard termination. 
                     " AssureWriteWithTermChar = True")  # Be sure to have all commands terminated with \n
sleep(1)
idn = instr.query_str('*IDN?')
print(f"\nHello, I am: '{idn}'")

# We assume the following amplitude values to be defined for a triangle waveform:
# 0 / 32767 / 0 / -32768 / 0
bin_data = bytes([00, 00, 0x7F, 0xFF, 00, 00, 0x80, 00, 00, 00])
instr.write_bin_block("DATA ", bin_data)  # Transfer the ARB data to the instrument
instr.write_str('FREQ 3000')  # Set Frequency to 3 kHz
instr.write_str('VOLT 2')  # Voltage is 2 V(pp) now
instr.write_str('FUNC:ARB RAM')  # Arbitrary function working from memory
instr.query_opc()
instr.write_str('FUNC ARB')  # Change to ARB mode
instr.write_str('OUTP ON')  # Switch output on
instr.query_opc()

print('\n')
print('Arb File transferred to memory,  ARB mode is active, output state is ON')

instr.close()  # And close the connection finally
