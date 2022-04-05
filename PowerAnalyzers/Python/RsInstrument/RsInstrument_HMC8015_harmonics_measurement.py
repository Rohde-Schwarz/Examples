"""

Created on 2022/03

Author: Jahns_P
Version Number: 1
Date of last change: 2022/03/31
Requires: HMC8015, FW 1.403 or newer and adequate options
- Installed RsInstrument Python module (see the attached RsInstrument_PythonModule folder Readme.txt)
- Installed VISA e.g. R&S Visa 5.12.x or newer

Description: Example for harmonic measurement readout


General Information:

Please always check this example script for unsuitable setting that may
destroy your DUT before connecting it to the instrument!
This example does not claim to be complete. All information has been
compiled with care. However errors can not be ruled out.
"""

from RsInstrument.RsInstrument import *
from time import sleep

# ================================
# Prepare instrument communication
# ================================

resource = 'TCPIP::10.205.0.53::5025::SOCKET'
hmc = RsInstrument(resource, True, True)
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
# Prepare instrument for harmonic measurement
# ===========================================

hmc.write('VIEW HARM')  # Change to harmonic View
hmc.write('VIEW:HARM:VIEW TABL')  # Format = Table
hmc.write('VIEW:HARM:SOURce VOLT')  # Define measurement source (BOTH / CURR / VOLT)
hmc.write('VIEW:HARM:NUMB 9')  # Set the number of harmonics to be captured
hmc.write('VIEW:HARM:SCAL ABS')  # Display format in relation to the fundamental (PERC / ABS)
hmc.write('VIEW:HARM:SUBS ODD')  # Define what type of harmonics to be displayed (ODD / EVEN / BOTH)
hmc.query_opc()
hmc.write('CHANnel1:MEASurement:FUNC UK1,IK1,PK1,UK3,IK3,PK3,UK5,IK5,PK5')  # Define readout order
# UKn = RMS Voltage of harmonic n
# IKn = RMS Current of harmonic n
# PKn = Active Power of harmonic n
hmc.query_opc()
sleep(2)  #


# ================================
# Perform 2 measurements in a loop
# ================================
x = 0
while x < 2:
    measurement = hmc.query_str('CHANnel1:MEASurement:DATA?')  # Reading of page 1
    print()
    print("========================================================"
          "========================================================")
    print("Original read string:")
    print(measurement)
    print()
    
    # --> This is how it could got split into substrings if necessary
    
    measurement = measurement.split(',')  # Split reading into a list
    uk1 = measurement[0]  # Allocate reading into sub variables
    ik1 = measurement[1]
    pk1 = measurement[2]
    uk3 = measurement[3]
    ik3 = measurement[4]
    pk3 = measurement[5]
    uk5 = measurement[6]
    ik5 = measurement[7]
    pk5 = measurement[8]

    print("========================================================"
          "========================================================")
    print()
    print('Actual reading:')
    print()
    print('RMS Voltage fundam. = '+uk1+' V')
    print('RMS Current fundam. = '+ik1+' A')
    print('Real Power  fundam. = '+pk1+' W')
    print('RMS Voltage harm. 3 = '+uk3+' V')
    print('RMS Current harm. 3 = '+ik3+' A')
    print('Real Power  harm. 3 = '+pk3+' W')
    print('RMS Voltage harm. 5 = '+uk5+' V')
    print('RMS Current harm. 5 = '+ik5+' A')
    print('Real Power  harm. 5 = '+pk5+' W')
    print('=============================')
    x = x+1
# =================
# Close the session
# =================

hmc.close()
