"""

Created on 2022/02

Author: Jahns_P
Version Number: 1
Date of last change: 2022/02/03
Requires: NRX, FW 02.50.21112602 or newer , adequate sensor and signal source
- Installed RsInstrument Python module (see the attached RsInstrument_PythonModule folder Readme.txt)
- Installed VISA e.g. R&S Visa 5.12.x or newer

Description: Example for single triggered measurement with marker support

General Information:

Please always check this example script for unsuitable setting that may
destroy your DUT or instrument before connecting!
This example does not claim to be complete. All information has been
compiled with care. However errors can not be ruled out.
"""

from RsInstrument import *
from time import sleep

RsInstrument.assert_minimum_version('1.9.0')

#
# Signal for the following settings is pulse modulated, 1m s PRI, 10 µs duty
#

nrp = RsInstrument('TCPIP::10.205.0.82::hislip0', True, True, "SelectVisa='rs'")
'''
(resource, True, True, "SelectVisa='rs'") has the following meaning:
(VISA-resource, id_query, reset, options)
- id_query: if True: the instrument's model name is verified against the models 
supported by the driver and eventually throws an exception.   
- reset: Resets the instrument (sends *RST) command and clears its status syb-system
- option SelectVisa:
    - 'SelectVisa = 'socket' - uses no VISA implementation for socket connections - you do not need any VISA-C installation
    - 'SelectVisa = 'rs' - forces usage of Rohde&Schwarz Visa
    - 'SelectVisa = 'ni' - forces usage of National Instruments Visa     
'''

sensor = nrp.query_str('SENS:CAT?')  # Request for connected sensor(s)
print('The following sensor is connected:', sensor)
print('Now performing Zeroing - please remove signal source from the sensor and confirm')
_ = input()
print('...Please wait until zeroing is done...')
nrp.write_str_with_opc('CAL1:ZERO ONCE')  # Perform Zeroing for all connected sensors
print('\nZeroing completed - please connect signal source to the sensor')
_ = input()
nrp.write_str_with_opc('DISPlay:LAYout L1')  # Display contains just one window
nrp.write_str_with_opc('CALCulate1:TYPE TRACe')  # Switch to Trace Mode
nrp.write_str('Sense1:TRACe:TIME .0002')  # Set displayed time range (10 times of time/div)
nrp.write_str_with_opc('FREQ 1GHz')  # Set working frequency (important for internal correction)
nrp.write_str_with_opc('TRIGger1:MODE SINGle')  # Single trigger mode
nrp.write_str('TRIGger1:CHAN1:LEV -21')  # Trigger level
nrp.write_str_with_opc('DISPlay1:TRACe:MARKer1:MODE MEASure')  # Show triangle on marker position
nrp.write_str_with_opc('DISPlay1:TRACe:MARKer1:POSition:MODE PSE')  # Peak search on for marker measurement
nrp.write_str_with_opc('DISPlay:WINDow1:Trace:MARKer:SELection M1')  # Shows the marker in the trace
nrp.write_str_with_opc('CALCulate1:DMODe MARKer')  # Switch display mode to marker display (from info mode)

sleep(.01)
x = 0
while x < 1000:
    level = nrp.query_str('CALC1:TRAC:MARK1:YPOS?')  # Request marker amount in dBm
    print('current measured level is ', level, ' dBm')
    x += 1
    if x == 5:
        break
    nrp.write_str_with_opc('INITiate1:IMMediate')  # Reset trigger state (wait for new event when in single trigger mode)
    sleep(1)
