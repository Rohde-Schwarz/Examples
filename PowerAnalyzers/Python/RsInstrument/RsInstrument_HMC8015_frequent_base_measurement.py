"""
# GitHub examples repository path: PowerAnalyzers/Python/RsInstrument

Created on 2020/09

Author: Jahns_P
Version Number: 3
Date of last change: 2022/03/31
Requires: HMC8015, FW 1.403 or newer and adequate options
- Installed RsInstrument Python module (see the attached RsInstrument_PythonModule folder Readme.txt)
- Installed VISA e.g. R&S Visa 5.12.x or newer

Description: Example for repetitive measurements


General Information:

Please always check this example script for unsuitable setting that may
destroy your DUT before connecting it to the instrument!
This example does not claim to be complete. All information has been
compiled with care. However, errors can not be ruled out.
"""

from RsInstrument.RsInstrument import *

# ================================
# Prepare instrument communication
# ================================

resource = 'TCPIP::10.205.0.97::5025::SOCKET'
HMC8015 = RsInstrument(resource, True, False)
HMC8015.visa_timeout = 3000  # Timeout for VISA Read Operations
HMC8015.opc_timeout = 3000  # Timeout for opc-synchronised operations
HMC8015.instrument_status_checking = True  # Error check after each command
HMC8015.clear_status()  # Clear status register
HMC8015.reset()  # Reset the instrument

# ============================================
# Do the first readout and get instrument data
# ============================================

idn = HMC8015.query_str('*IDN?')
print(f"\nHello, I am: '{idn}'")  # Identification String
print(f'RsInstrument driver version: {HMC8015.driver_version}')  # Rest is self explaining
print(f'Visa manufacturer: {HMC8015.visa_manufacturer}')
print(f'Instrument full name: {HMC8015.full_instrument_model_name}')
print(f'Instrument installed options: {",".join(HMC8015.instrument_options)}')

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
HMC8015.write_str_with_opc('VIEW:NUMeric:PAGE1:CELL1:FUNCtion URMS')  # Page1 Cell1 to root mean square voltage
HMC8015.write_str_with_opc('VIEW:NUMeric:PAGE1:CELL2:FUNCtion P')  # Page1 Cell2 to average voltage
HMC8015.write_str_with_opc('VIEW:NUMeric:PAGE1:CELL3:FUNCtion Q')  # Page1 Cell3 to root mean square current
HMC8015.write_str_with_opc('VIEW:NUMeric:PAGE1:CELL4:FUNCtion IRMS')  # Page1 Cell4 to average current
HMC8015.write_str_with_opc('VIEW:NUMeric:PAGE1:CELL5:FUNCtion FU')  # Page1 Cell5 to active power
HMC8015.write_str_with_opc('VIEW:NUMeric:PAGE1:CELL6:FUNCtion FI')  # Page1 Cell6 to apparent power


# ==================================
# Perform 100 measurements in a loop
# ==================================
x = 0
while x < 100:
    measurement = HMC8015.query_str('CHANnel1:MEASurement:DATA?')  # Reading of page 1
    print()
    print("========================================================"
          "========================================================")
    print("Original read string:")
    print(measurement)
    print()
    
    # --> This is how it could got split into substrings if necessary
    
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
    x = x+1
# =================
# Close the session
# =================

HMC8015.close()
