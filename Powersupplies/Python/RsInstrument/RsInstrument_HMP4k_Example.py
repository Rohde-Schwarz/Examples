# GitHub examples repository path: Powersupplies/Python/RsInstrument
# Example on how to use the RsInstrument module for remote-controlling your instrument
# Preconditions:
# - Installed RsInstrument Python module from pypi.org
# - Installed VISA e.g. R&S Visa 5.12.x or newer

from RsInstrument import *  # The RsInstrument package is hosted on pypi.org, see Readme.txt for more details

# Make sure you have the last version of the RsInstrument
RsInstrument.assert_minimum_version('1.22.0')

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
