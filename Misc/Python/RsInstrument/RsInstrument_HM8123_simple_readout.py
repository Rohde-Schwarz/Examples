"""

Created on 2021/11

Author: Jahns_P
Version Number: 1
Date of last change: 2021/11/05
Requires: R&S HM8123, FW 5.12 or newer
- Installed RsInstrument Python module (see https://rsinstrument.readthedocs.io/en/latest/)
- Installed VISA e.g. R&S Visa 5.12.x or newer

Description: Initiate Instrument and perform measurement on CH B


General Information:
This example does not claim to be complete. All information has been
compiled with care. However, errors can not be ruled out.
"""

from RsInstrument import *
from time import sleep


# Make sure you have the last version of the RsInstrument
RsInstrument.assert_minimum_version('1.22.0')
instr = RsInstrument('ASRL4::INSTR', options='Profile=hm8123')
instr.reset()
sleep(1)
idn = instr.query_str('IDN')
print(f"\nHello, I am: '{idn}'")
instr.write('FRB')                                  # Measurement Mode Frequency CH B
sleep(0.05)                                        # Additional pause might be necessary after the commands when running into problems
instr.write('SMT 10')                               # Set Gate Time to 10 ms
instr.write('WT0')                                  # Disable Wait Time
instr.write('DS0')                                  # Switch off Display for better performance
instr.write('TRG')                                  # Initiate Trigger
sleep(0.1)
value = instr.query_str('XMT')                      # Request measurement data
print(f'\nMeasurement value now is: ', value)
instr.close()                                       # And close the connection finally
