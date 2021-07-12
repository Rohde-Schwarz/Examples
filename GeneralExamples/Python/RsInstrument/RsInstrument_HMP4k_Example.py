# Simple example on how to use the RsInstrument module for remote-controlling yor VISA instrument
# Preconditions:
# - Installed RsInstrument Python module Version 1.15.0.68 or newer from pypi.org
# - Installed VISA e.g. R&S Visa 5.12.x or newer

from RsInstrument import *  # The RsInstrument package is hosted on pypi.org, see Readme.txt for more details

RsInstrument.assert_minimum_version('1.15.0.68')
instr = RsInstrument('TCPIP::10.205.0.41::5025::SOCKET', True, True)

idn = instr.query_str('*IDN?')
print(f"\nHello, I am: '{idn}'")
print(f'RsInstrument driver version: {instr.driver_version}')
print(f'Visa manufacturer: {instr.visa_manufacturer}')
print(f'Instrument full name: {instr.full_instrument_model_name}')
print(f'Instrument options: {instr.instrument_options}')
instr.visa_timeout = 2000


# Close the session
instr.close()
