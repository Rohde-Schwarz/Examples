"""Basic example of importing the package, initializing the session and performing basic generator settings."""

from RsSmab import *

RsSmab.assert_minimum_version('4.70.300')
smab = RsSmab('TCPIP::10.112.1.64::HISLIP')
# smab = RsSmab('TCPIP::10.112.0.106::5025::SOCKET', options='SelectVisa=SocketIo') # No VISA needed
print(f'Driver Info: {smab.utilities.driver_version}')
print(f'Instrument: {smab.utilities.idn_string}')

# Instrument options are properly parsed, and sorted (k-options first)
print(f'Instrument options: {",".join(smab.utilities.instrument_options)}')

# Driver's instrument status checking ( SYST:ERR? ) after each command (default value is True):
smab.utilities.instrument_status_checking = True

smab.output.state.set_value(True)
smab.source.frequency.set_mode(enums.FreqMode.CW)
smab.source.power.level.immediate.set_amplitude(-20)
smab.source.frequency.fixed.set_value(223E6)

# You can still use the direct SCPI interface:
response = smab.utilities.query_str('*IDN?')
print(f'Direct SCPI response on *IDN?: {response}')
smab.close()
