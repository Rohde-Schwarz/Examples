"""
# GitHub examples repository path: PowerAnalyzers/Python/RsInstrument

Created on 2020/03

Author: Jahns_P
Version Number: 5
Date of last change: 2022/03/31
Requires: HMC8015, FW 1.403 or newer and adequate options
- Installed RsInstrument Python module (see the attached RsInstrument_PythonModule folder Readme.txt)
- Installed VISA e.g. R&S Visa 5.12.x or newer

Description: Example for measurements and save a screenshot to local PC


General Information:

Please always check this example script for unsuitable setting that may
destroy your DUT before connecting it to the instrument!
This example does not claim to be complete. All information has been
compiled with care. However, errors can not be ruled out.
"""

from RsInstrument.RsInstrument import *
from time import sleep


# ================================
# Prepare instrument communication
# ================================

resource = 'TCPIP::10.205.0.53::5025::SOCKET'
hmc = RsInstrument(resource, True, False)
hmc.visa_timeout = 3000  # Timeout for VISA Read Operations
hmc.opc_timeout = 3000  # Timeout for opc-synchronised operations
hmc.instrument_status_checking = True  # Error check after each command
hmc.clear_status()  # Clear status register
hmc.reset()  # Reset the instrument


# ============================================
# Do the first readout and get instrument data
# ============================================

idn = hmc.query_str('*IDN?')
print(f"\nHello, I am: '{idn}'")  # Identification String
print(f'RsInstrument driver version: {hmc.driver_version}')  # Rest is self explaining
print(f'Visa manufacturer: {hmc.visa_manufacturer}')
print(f'Instrument full name: {hmc.full_instrument_model_name}')
print(f'Instrument installed options: {",".join(hmc.instrument_options)}')


# ===========================================
# Prepare instrument for desired measurements
# ===========================================

'''
There are four measurement windows with 6 cells each available
Command is "VIEW:NUMeric:PAGE<n>:CELL<m>:FUNCtion?"

Where <n> is number of page (1...4)
and   <m> is number of cell (1...6-10)
With functions

P Active power P (Watt)
S Apparent power S (VA)
Q Reactive power Q (var)
LAMBda Power factor λ (PF)
PHI Phase difference Φ ( ° )
FU Voltage frequency fU (V)
FI Current frequency fI (A)
URMS True rms voltage Urms (V)
UAVG Voltage average (V)
IRMS True rms current Irms (A)
IAVG Current average (A)
UTHD Total harmonic distortion of voltage Uthd (THD %)
ITHD Total harmonic distortion of current Ithd (THD %)
FPLL PLL source frequency fPLL (Hz)
TIME Integration time
WH Watt hour (Wh)
WHP Positive watt hour (Wh)
WHM Negative watt hour (Wh)
AH Ampere hour (Ah)
AHP Positive ampere hour (Ah)
AHM Negative ampere hour (Ah)
URANge Voltage range
IRANge Current range
EMPTy Empty cell
'''
hmc.write_str_with_opc('VIEW:NUMeric:PAGE1:CELL1:FUNCtion URMS')            # Page1 Cell1 to root mean square voltage
hmc.write_str_with_opc('VIEW:NUMeric:PAGE1:CELL2:FUNCtion UAVG')            # Page1 Cell2 to average voltage
hmc.write_str_with_opc('VIEW:NUMeric:PAGE1:CELL3:FUNCtion IRMS')            # Page1 Cell3 to root mean square current
hmc.write_str_with_opc('VIEW:NUMeric:PAGE1:CELL4:FUNCtion IAVG')            # Page1 Cell4 to average current
hmc.write_str_with_opc('VIEW:NUMeric:PAGE1:CELL5:FUNCtion P')               # Page1 Cell5 to active power
hmc.write_str_with_opc('VIEW:NUMeric:PAGE1:CELL6:FUNCtion S')               # Page1 Cell6 to apparent power


# ========================
# Perform the measurements
# ========================

sleep(3)
measurement = hmc.query_str('CHANnel1:MEASurement:DATA?')  # Reading of page 1
print()
print("========================================================"
      "========================================================")
print("Original read string:")
print(measurement)
print()
measurement = measurement.split(',')  # Split reading into a list
urms = measurement[0]  # Allocate reading into sub variables
uavg = measurement[1]
irms = measurement[2]
iavg = measurement[3]
powr = measurement[4]
powapp = measurement[5]

print("========================================================"
      "========================================================")
print()
print('Actual reading:')
print()
print('RMS Voltage    = '+urms+' V')
print('Avg Voltage    = '+uavg+' V')
print('RMS Current    = '+irms+' V')
print('Avg Current    = '+iavg+' V')
print('Active Power   = '+powr+' V')
print('Apparent Power = '+powapp+' V')
print('=============================')


# ======================
# Now get the screenshot
# ======================

hmc.write_str_with_opc('HCOPy:FORMat BMP')  # Hard copy file format to BMP
hmc.query_bin_block_to_file('HCOPy:DATA?', r"e:\Python\Dev_Screenshot.bmp", False)  # Transfer file to PC
print(r'\nScreenshot saved to e:\Python\Dev_Screenshot.bmp')


# =================
# Close the session
# =================

hmc.close()
