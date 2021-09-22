# Simple example on how to use the RsInstrument module for remote-controlling of your instrument
# Preconditions:
# - Installed RsInstrument Python module Version 1.17.0.72 or newer from pypi.org
# - Installed VISA e.g. R&S Visa 5.12.x or newer

from RsInstrument import *  # The RsInstrument package is hosted on pypi.org, see Readme.txt for more details

resource_string_1 = 'TCPIP::localhost::5025::SOCKET'  # Standard LAN connection (also called VXI-11)
resource_string_2 = 'TCPIP::192.168.2.101::hislip0'  # Hi-Speed LAN connection - see 1MA208
resource_string_3 = 'GPIB::20::INSTR'  # GPIB Connection
resource_string_4 = 'USB::0x0AAD::0x0119::022019943::INSTR'  # USB-TMC (Test and Measurement Class)
resource_string_5 = 'RSNRP::0x0095::104015::INSTR'  # R&S Powersensor NRP-Z86
resource_string_6 = 'DEVICE'  # Symbolic name in Visa Configuration file

option_string_empty = ''  # Default setting
option_string_force_ni_visa = 'SelectVisa=ni'  # Forcing NI VISA usage
option_string_force_rs_visa = 'SelectVisa=rs'  # Forcing R&S VISA usage
option_string_force_no_visa = 'SelectVisa=SocketIo'  # Socket communication for LAN connections, no need for any VISA installation

RsInstrument.assert_minimum_version('1.17.0.72')
instr = RsInstrument(resource_string_6, True, False, option_string_empty)

idn = instr.query_str('*IDN?')
print(f"\nHello, I am: '{idn}'")
print(f'RsInstrument driver version: {instr.driver_version}')
print(f'Visa manufacturer: {instr.visa_manufacturer}')
print(f'Instrument full name: {instr.full_instrument_model_name}')
print(f'Instrument installed options: {",".join(instr.instrument_options)}')

# Close the session
instr.close()
