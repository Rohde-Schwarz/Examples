"""
# GitHub examples repository path: Powersupplies/Python/RsInstrument

Created on 2023/04

Author: Customer Support / PJ
Version Number: 1
Date of last change: 2023/04/12
Requires:
- R&S NGM / NGL FW 04.00 or newer
- Option K102 (for SN° < 110000) for remote control
- Option K103 for Digital Trigger I/O
- A trigger source (e.g. Arduino board with "Blink" example), if not available use *TRG command as described below
- Trigger source must be connected to PIN 8 (GND) and PIN 3 (TRIGGER IN) of the SUB-D15 Digital I/O connector
- Installed RsInstrument Python module (see https://rsinstrument.readthedocs.io/en/latest/)
- Installed VISA e.g. R&S Visa 5.12.x or newer

Description: Initiate Instrument, define ARB sequence, let it run once, change to stepped triggered mode


General Information:
This example does not claim to be complete. All information has been
compiled with care. However, errors can not be ruled out.
"""

from RsInstrument import *
from time import sleep

# Initiate instrument connection
ngm = RsInstrument('TCPIP::10.205.0.76::hislip0', reset=True)
resp = ngm.query_opc()  # Check for Reset operation to be complete

# ARB definition
ngm.write('INSTrument:SELect OUT1')  # Select Output 1 (CH1) for allocation of the next commands
ngm.write('ARB:CLEAR')  # Clear ARB memory for selected channel
# Set 4 ARB data points with the following definition each: Voltage, Current, Time, Interpolation mode on or off
ngm.write('ARB:DATA 3.3,1,1,0,3,1,1,0,2,1,1,0,1.5,1,1,0') # 3,3 V, 1 A, 1 s, no interpolation, 3 V, etc...
ngm.write('ARB:REP 2')  # Sequence will run two times
ngm.write('ARB:BEH:END HOLD')  # Channel will hold the last voltage level after the sequence is done
ngm.write('ARB:TRAN 1')  # Transfer ARB data to CH1
ngm.write('ARBitrary:FNAMe "ARBFILE.CSV", INT')  # Defines the name of the ARB sequence file on the instrument
ngm.write('ARBitrary:SAVE')  # Saves the file to the instrument. Load files with "ARB:FNAME" and "ARB:LOAD"
ngm.query_opc()  # Check for operation(s) to be complete

# Start the defined sequence
ngm.write('ARBitrary 1')  # Initiate the sequence in CH1
ngm.write('OUTPut:STATe ON')  # Switch on the output and start the ARB sequence
sleep(9)  # Wait for nine seconds for the arb sequence to be done two times and have 1 additional second for a pause
ngm.write('OUTPut:STATe OFF')  # Sequence is done, switch output off

# Now use stepped trigger to run the ARB sequence with external signal (Triggers on both rising and falling edge!).
# The specified voltages are 0 V to 15 V for all input pins.
# As an alternative to the external trigger signal the same setup can be used for software trigger.
# Soft trigger is initiated by sending the "*TRG" command to the instrument.
ngm.write('ARBitrary:TRIGgered:MODE SINGle')  # A single trigger event only starts one step of the sequence
ngm.write('ARBitrary:TRIGgered:STATe ON')  # Change ARB to triggered mode
ngm.write('TRIGger:SEQuence:IMMediate:SOURce DIO')  # Trigger source now is DIO
ngm.write('TRIGger:SEQuence:IMMediate:SOURce:DIO:PIN IN')  #
ngm.write('ARBitrary 1')  # Activate ARB for CH1 again
ngm.write('TRIGger:STATe 1')  # Enable the trigger system
ngm.query_opc()  # Check for operation complete
ngm.write('OUTPut:STATe ON')  # Switch on the output and start the ARB sequence
sleep(30)  # let it run for 30 seconds
ngm.write('OUTPut:STATe OFF')  # Sequence is done, switch output off

ngm.close()  # Close instrument connection

print('Program finished with success')
