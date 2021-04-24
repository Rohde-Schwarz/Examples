"""Basic example of importing the package, initializing the session and performing basic generator settings."""

from RsSmbv import *

RsSmbv.assert_minimum_version('4.80.2')
smbv = RsSmbv('TCPIP::10.112.0.228::HISLIP')
# smbv = RsSmbv('TCPIP::10.112.1.179::5025::SOCKET', options='SelectVisa=SocketIo') # No VISA needed
print(f'Driver Info: {smbv.utilities.driver_version}')
print(f'Instrument: {smbv.utilities.idn_string}')

# Instrument options are properly parsed, and sorted (k-options first)
print(f'Instrument options: {",".join(smbv.utilities.instrument_options)}')

# Driver's instrument status checking ( SYST:ERR? ) after each command (default value is True):
smbv.utilities.instrument_status_checking = True

smbv.output.state.set_value(True)
smbv.source.frequency.set_mode(enums.FreqMode.CW)
smbv.source.power.level.immediate.set_amplitude(-20)
smbv.source.frequency.fixed.set_value(223E6)
print(f'PEP level: {smbv.source.power.get_pep()} dBm')

# You can still use the direct SCPI interface:
response = smbv.utilities.query_str('*IDN?')
print(f'Direct SCPI response on *IDN?: {response}')
smbv.close()
