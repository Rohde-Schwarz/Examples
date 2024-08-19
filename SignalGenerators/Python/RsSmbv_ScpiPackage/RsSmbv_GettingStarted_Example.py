"""
Getting started - how to work with RsSmbv Python package.
This example performs basic RF settings on an SMBV100B instrument.
It shows the RsSmbv calls and their corresponding SCPI commands.
Notice that the python RsSmbv interfaces track the SCPI commands syntax.

RsSmbv documentation: https://rohde-schwarz.github.io/RsSmbv_PythonDocumentation/index.html
"""

from RsSmbv import *

# Open the session
smbv = RsSmbv('TCPIP::192.168.1.100::hislip0')
# Greetings, stranger...
print(f'Hello, I am: {smbv.utilities.idn_string}')

#   OUTPut:STATe ON
smbv.output.state.set_value(True)

#   SOURce:FREQuency:MODE CW
smbv.source.frequency.set_mode(enums.FreqMode.CW)

#   SOURce:POWer:LEVel:IMMediate:AMPLitude -20
smbv.source.power.level.immediate.set_amplitude(-20)

#   SOURce:FREQuency:FIXed 223000000
smbv.source.frequency.fixed.set_value(223E6)

#         SOURce:POWer:PEP?
pep = smbv.source.power.get_pep()
print(f'PEP level: {pep} dBm')


# Close the session
smbv.close()
