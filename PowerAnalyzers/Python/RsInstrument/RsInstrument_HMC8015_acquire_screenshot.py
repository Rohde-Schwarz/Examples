"""

Created on 2021/06

Author: Jahns_P
Version Number: 1
Date of last change: 2022/03/31
Requires: HMC8015, FW 1.403 or newer and adequate options
- Installed RsInstrument Python module (see the attached RsInstrument_PythonModule folder Readme.txt)
- Installed VISA e.g. R&S Visa 5.12.x or newer

Description: Example on how to get a screenshot to PC


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
HMC8015 = RsInstrument(resource, False, False)
HMC8015.visa_timeout = 3000  # Timeout for VISA Read Operations
HMC8015.opc_timeout = 3000  # Timeout for opc-synchronised operations
HMC8015.instrument_status_checking = True  # Error check after each command
HMC8015.clear_status()  # Clear status register

# ============================================
# Do the first readout and get instrument data
# ============================================

idn = HMC8015.query_str('*IDN?')
print(f"\nHello, I am: '{idn}'")  # Identification String
print(f'RsInstrument driver version: {HMC8015.driver_version}')  # Rest is self explaining
print(f'Visa manufacturer: {HMC8015.visa_manufacturer}')
print(f'Instrument full name: {HMC8015.full_instrument_model_name}')
print(f'Instrument installed options: {",".join(HMC8015.instrument_options)}')

# ======================
# Now get the screenshot
# ======================

HMC8015.write_str_with_opc('HCOPy:FORMat BMP')  # Hard copy file format to BMP
HMC8015.query_bin_block_to_file('HCOPy:DATA?', r"e:\Python\Dev_Screenshot.png", False)  # Transfer file to PC
print()
print('Successfully saved the screenshot to E:\Python\Dev_Screenshot.png')


# =================
# Close the session
# =================

HMC8015.close()
