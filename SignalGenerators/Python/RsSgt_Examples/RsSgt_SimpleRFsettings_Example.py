"""Basic example of importing the package, initializing the session and performing basic generator settings."""

from RsSgt import *


sgt = RsSgt('TCPIP::10.112.1.73::HISLIP')
# sgt = RsSgt('TCPIP::10.214.1.57::5025::SOCKET', options='SelectVisa=SocketIo') # No VISA needed
print(f'Driver Info: {sgt.utilities.driver_version}')
print(f'Instrument: {sgt.utilities.idn_string}')

# Instrument options are properly parsed, and sorted (k-options first)
print(f'Instrument options: {",".join(sgt.utilities.instrument_options)}')

# Driver's instrument status checking ( SYST:ERR? ) after each command (default value is True):
sgt.utilities.instrument_status_checking = True

sgt.output.state.set_value(True)
sgt.source.power.level.immediate.set_amplitude(-20)
sgt.source.frequency.fixed.set_value(223E6)
print(f'PEP level: {sgt.source.power.get_pep()} dBm')

# You can still use the direct SCPI interface:
response = sgt.utilities.query_str('*IDN?')
print(f'Direct SCPI response on *IDN?: {response}')
sgt.close()
