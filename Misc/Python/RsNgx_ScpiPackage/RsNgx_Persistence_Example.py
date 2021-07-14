""""RsNgx example showing how to use channel persistence feature."""

import time
from RsNgx import *

RsNgx.assert_minimum_version('3.0.0.38')
ngx = RsNgx('TCPIP::10.102.52.45::INSTR')
print(f'Hello, I am: {ngx.utilities.idn_string}')
print(f'My installed options: {ngx.utilities.instrument_options}')
ngx.utilities.reset()

# Master switch for all the outputs - switch OFF
ngx.output.general.set_state(False)

# We clone the ngx object to ngx_ch1 and switch channel persistence to output channel 1
# It means, the driver makes sure that every command you sent with the ngx_ch1 goes to output channel 1
ngx_ch1 = ngx.clone()
ngx_ch1.set_persistent_channel(1)

# Now we do the same for output channel 2
ngx_ch2 = ngx.clone()
ngx_ch2.set_persistent_channel(2)

# We can now use the ngx_ch1 and ngx_ch2 in any order, without having to call ngx.instrument.select.set() in between:
ngx_ch1.source.voltage.level.immediate.set_amplitude(3.3)
ngx_ch2.source.voltage.level.immediate.set_amplitude(1.1)
ngx_ch1.source.current.level.immediate.set_amplitude(0.11)
ngx_ch2.source.current.level.immediate.set_amplitude(0.22)
# Only Output 1 is ON
ngx_ch1.output.set_select(True)
# Output 2 stays OFF
ngx_ch2.output.set_select(False)

# For commands that are not channel - related, like for example reset() or Master switch (below),
# you can use any of the objects: ngx, ngx_ch1, ngx_ch2
ngx.output.general.set_state(True)
# Insert a small pause to allow the instrument to settle the output
time.sleep(0.5)

# Read the measurement on both outputs:
measurement = ngx_ch1.read()
print(f'Measured values Output 1: {measurement.Voltage} V, {measurement.Current} A')
# Output 2 is not ON, we get NAN readings
measurement = ngx_ch2.read()
print(f'Measured values Output 2: {measurement.Voltage} V, {measurement.Current} A')

# In order to close the VISA session, you need to call the close() on the original object 'ngx'
# Calling close() on the cloned objects 'ngx_ch1' or 'ngx_ch2' does not close the original VISA session:
ngx_ch1.close()
print(f'I am alive and well and can call reset() ...')
ngx.utilities.reset()
ngx_ch2.close()
print(f'I can still switch the master OFF ...')
ngx.output.general.set_state(False)
ngx.close()
print(f'Finally, you destroyed me...')
