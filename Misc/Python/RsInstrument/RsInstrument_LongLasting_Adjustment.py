# Example on how to use the RsInstrument module for remote-controling of your instrument
# Here we show on how to perform a long-lasting operation, like for example an instrument calibration
# Preconditions:
# - Installed RsInstrument Python module
# - Installed VISA e.g. R&S Visa 5.12.x or newer

from RsInstrument import *  # The RsInstrument package is hosted on pypi.org, see Readme.txt for more details

instr_resource_string = 'TCPIP::10.112.1.179::HISLIP'
option_string_empty = ''
option_string_force_ni_visa = 'SelectVisa=ni'  # Forcing NI VISA usage
option_string_force_rs_visa = 'SelectVisa=rs'  # Forcing R&S VISA usage
option_string_force_no_visa = 'SelectVisa=SocketIo'  # Socket communication for LAN connections, no need for any VISA installation

# Make sure you have the last version of the RsInstrument
RsInstrument.assert_minimum_version('1.22.0')

instr = RsInstrument(instr_resource_string, True, False, option_string_empty)

idn = instr.query_str('*IDN?')
print(f"\nInstrument: '{idn}'")
print(f'RsInstrument driver version: {instr.driver_version}')
print(f'Visa manufacturer: {instr.visa_manufacturer}')
print(f'Installed options: {",".join(instr.instrument_options)}')

# Start the alignment
cal_timeout_secs = 240
print(f'Starting instrument complete alignment, timeout {cal_timeout_secs} seconds...')
result = instr.query_str_with_opc('CAL:ALL:MEAS?', cal_timeout_secs * 1000)
print(f'Finished with result {result}')
print('Closing the instrument session')

# Close the session
instr.close()
