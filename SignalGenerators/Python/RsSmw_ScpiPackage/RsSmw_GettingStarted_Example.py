"""
Getting started - how to work with RsSmw Python package.
This example performs basic RF settings on an SMW200A instrument.
It shows the RsSmw calls and their corresponding SCPI commands.
Notice that the python RsSmw interfaces track the SCPI commands syntax.

RsSmw documentation: https://rohde-schwarz.github.io/RsSmw_PythonDocumentation/index.html
"""

from RsSmw import *

# Open the session
smw = RsSmw('TCPIP::192.168.1.100::hislip0')
# Greetings, stranger...
print(f'Hello, I am: {smw.utilities.idn_string}')

# Print commands to the console with the logger
smw.utilities.logger.mode = LoggingMode.On
smw.utilities.logger.log_to_console = True

#   OUTPut1:STATe ON
smw.output.state.set_value(True)

#   SOURce1:FREQuency:MODE CW
smw.source.frequency.set_mode(enums.FreqMode.CW)

#   SOURce1:POWer:LEVel:IMMediate:AMPLitude -20
smw.source.power.level.immediate.set_amplitude(-20)

#   SOURce1:FREQuency:FIXed 223000000
smw.source.frequency.fixed.set_value(223E6)

#         SOURce1:POWer:PEP?
pep = smw.source.power.get_pep()
print(f'Channel 1 PEP level: {pep} dBm')

# Change the output to B (default is A):
smw.repcap_hwInstance_set(repcap.HwInstance.InstB)

# Now we are addressing output B
#   OUTPut2:STATe ON
smw.output.state.set_value(True)

#         SOURce2:POWer:PEP?
pep = smw.source.power.get_pep()
print(f'Channel 2 PEP level: {pep} dBm')

# Close the session
smw.close()
