"""
Basic example of importing the package, initializing the session and performing basic generator settings.

RsSmw documentation: https://rohde-schwarz.github.io/RsSmw_PythonDocumentation/index.html
"""


from RsSmw import *

RsSmw.assert_minimum_version('5.0.44')
smw = RsSmw('TCPIP::192.168.1.100::hislip0')
# smw = RsSmw('TCPIP::10.112.1.179::5025::SOCKET', options='SelectVisa=SocketIo') # No VISA needed
print(f'Driver Info: {smw.utilities.driver_version}')
print(f'Instrument: {smw.utilities.idn_string}')

# Instrument options are properly parsed duplicates are removed, and the items are sorted (k-options first)
print(f'Instrument options: {",".join(smw.utilities.instrument_options)}')

# Driver's instrument status checking ( SYST:ERR? ) after each command (default value is True):
smw.utilities.instrument_status_checking = True

# The smw object uses the global HW instance one - RF out A
smw.repcap_hwInstance_set(repcap.HwInstance.InstA)

# Clone the smw object to the smw_rf2 and select the RF out B
smw_rf2 = smw.clone()
smw_rf2.repcap_hwInstance_set(repcap.HwInstance.InstB)

# Now we have two independent objects for two RF Outputs - smw and smw_rf2
# They share some common features of the instrument, like for example resetting
smw_rf2.utilities.reset()

smw.output.state.set_value(True)
smw.source.frequency.set_mode(enums.FreqMode.CW)
smw.source.power.level.immediate.set_amplitude(-20)
smw.source.frequency.fixed.set_value(223E6)
print(f'Channel 1 PEP level: {smw.source.power.get_pep()} dBm')

smw_rf2.output.state.set_value(False)
smw_rf2.source.frequency.set_mode(enums.FreqMode.SWEep)
smw_rf2.source.power.level.immediate.set_amplitude(-35)
smw_rf2.source.frequency.set_start(800E6)
smw_rf2.source.frequency.set_stop(900E6)
smw_rf2.source.frequency.step.set_mode(enums.FreqStepMode.DECimal)
smw_rf2.source.frequency.step.set_increment(10E6)
print(f'Channel 2 PEP level: {smw_rf2.source.power.get_pep()} dBm')

# Direct SCPI interface:
response = smw.utilities.query_str('*IDN?')
print(f'Direct SCPI response on *IDN?: {response}')
smw.close()
