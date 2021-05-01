""""RsNgx basic example - sets Voltage, Current limit and output state on two output channels."""

import time
from RsNgx import *

ngx = RsNgx('TCPIP::10.102.52.45::INSTR')
# Greetings, stranger...
print(f'Hello, I am: {ngx.utilities.idn_string}')
ngx.utilities.reset()

# Master switch for all the outputs - switch OFF
ngx.output.general.set_state(False)

# Select and set Output 1
ngx.instrument.select.set(1)
ngx.source.voltage.level.immediate.set_amplitude(3.3)
ngx.source.current.level.immediate.set_amplitude(0.1)
# Prepare for setting the output to ON with the master switch
ngx.output.set_select(True)

# Select and set Output 2
ngx.instrument.select.set(2)
ngx.source.voltage.level.immediate.set_amplitude(5.1)
ngx.source.current.level.immediate.set_amplitude(0.05)
# Prepare for setting the output to ON with the master switch
ngx.output.set_select(True)

# The outputs are still not ON, they wait for this master switch:
ngx.output.general.set_state(True)
# Insert a small pause to allow the instrument to settle the output
time.sleep(0.5)

ngx.instrument.select.set(1)
measurement = ngx.get_read()
print(f'Measured values Output 1: {measurement.Voltage} V, {measurement.Current} A')

ngx.instrument.select.set(2)
measurement = ngx.get_read()
print(f'Measured values Output 2: {measurement.Voltage} V, {measurement.Current} A')
ngx.close()