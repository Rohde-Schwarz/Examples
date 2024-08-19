"""
# GitHub examples repository path: SignalGenerators/Python/RsInstrument

This is a Hello-World example for communicating with your SMBxxx instrument.
Sets Output Frequency and Power, then sets the output state to ON.
RsInstrument documentation: https://rsinstrument.readthedocs.io/en/latest/
"""

# RsInstrument package is hosted on pypi.org
from RsInstrument import *

# Initialize the session
smb = RsInstrument('TCPIP::192.168.1.100::hislip0')

print(f"\nHello, I am: '{smb.idn_string}'")
print(f'Instrument installed options: {",".join(smb.instrument_options)}')

# Enter your code here...
smb.write('SOURce:FREQuency:CW 2200000000')
smb.write('SOURce:POWer:POWer -25.5')
smb.write('OUTPut:STATe ON')

# Close the session
smb.close()
