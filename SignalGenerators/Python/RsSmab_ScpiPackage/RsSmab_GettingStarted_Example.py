"""Getting started - how to work with RsSmab Python package.
This example performs basic RF settings on an SMA100B instrument.
It shows the RsSmab calls and their corresponding SCPI commands.
Notice that the python RsSmab interfaces track the SCPI commands syntax."""

from RsSmab import *

# Open the session
smab = RsSmab('TCPIP::10.112.1.67::HISLIP')
# Greetings, stranger...
print(f'Hello, I am: {smab.utilities.idn_string}')

#   OUTPut:STATe ON
smab.output.state.set_value(True)

#   SOURce:FREQuency:MODE CW
smab.source.frequency.set_mode(enums.FreqMode.CW)

#   SOURce:POWer:LEVel:IMMediate:AMPLitude -20
smab.source.power.level.immediate.set_amplitude(-20)

#   SOURce:FREQuency:FIXed 223000000
smab.source.frequency.fixed.set_value(223E6)

#         SOURce:POWer:PEP?
pep = smab.source.power.get_pep()
print(f'PEP level: {pep} dBm')


# Close the session
smab.close()
