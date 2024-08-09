"""Getting started - how to work with RsSgt Python package.
This example performs basic RF settings on an SGT100A instrument.
It shows the RsSgt calls and their corresponding SCPI commands.
Notice that the python RsSgt interfaces track the SCPI commands syntax."""

from RsSgt import *

# Open the session
sgt = RsSgt('TCPIP::192.168.1.100::hislip0')
# Greetings, stranger...
print(f'Hello, I am: {sgt.utilities.idn_string}')

#   OUTPut:STATe ON
sgt.output.state.set_value(True)

#   SOURce:POWer:LEVel:IMMediate:AMPLitude -25
sgt.source.power.level.immediate.set_amplitude(-25)

#   SOURce:FREQuency:FIXed 1100000000
sgt.source.frequency.fixed.set_value(1.1E9)

#         SOURce:POWer:PEP?
pep = sgt.source.power.get_pep()
print(f'PEP level: {pep} dBm')

# Close the session
sgt.close()
