"""Getting started - how to work with RsSmcv Python package.
This example performs basic RF settings on an SMCV100B instrument.
It shows the RsSmcv calls and their corresponding SCPI commands.
Notice that the python RsSmcv interfaces track the SCPI commands syntax."""

from RsSmcv import *

# Open the session
smcv = RsSmcv('TCPIP::10.112.0.228::HISLIP')
# Greetings, stranger...
print(f'Hello, I am: {smcv.utilities.idn_string}')

#   OUTPut:STATe ON
smcv.output.state.set_value(True)

#   SOURce:FREQuency:MODE CW
smcv.source.frequency.set_mode(enums.FreqMode.CW)

#   SOURce:POWer:LEVel:IMMediate:AMPLitude -20
smcv.source.power.level.immediate.set_amplitude(-20)

#   SOURce:FREQuency:FIXed 223000000
smcv.source.frequency.fixed.set_value(223E6)

#         SOURce:POWer:PEP?
pep = smcv.source.power.get_pep()
print(f'PEP level: {pep} dBm')


# Close the session
smcv.close()
