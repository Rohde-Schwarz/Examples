"""
This example acquires a signal on a MXO Oscilloscope, and performs the measurement of min/max peaks.
Additionally, the SCPI communication logger into the console shows you the SCPI communication with your MXO.
"""
from RsMxo import *
from RsMxo.enums import *


RsMxo.assert_minimum_version('2.6.4')

# Open the session - adjust the resource name to fit your instrument
mxo = RsMxo('TCPIP::192.168.1.101::hislip0', id_query=False)
# Greetings, stranger...
print(f'Hello, I am: {mxo.utilities.idn_string}')

# Print commands to the console with the logger
mxo.utilities.logger.mode = LoggingMode.On
mxo.utilities.logger.log_to_console = True

#   SYSTem:DISPlay:UPDate ON
mxo.system.display.set_update(True)

mxo.trigger.set_mode(trigger_mode=TriggerMode.AUTO)
mxo.acquire.symbolRate.set_mode(sample_rate_mode=AutoManualMode.AUTO)

mxo.channel.state.set(True)

# Perform the Acquisition
mxo.run.single_and_wait()

# Measurement can be done on an already existing acquired data.

# Measurement 1 - peak max
m1 = repcap.MeasIndex.Nr1
mxo.measurement.source.set(signal_source=enums.SignalSource.C1, measIndex=m1)
mxo.measurement.main.set(meas_type=MeasType.MAXimum, measIndex=m1)
mxo.measurement.enable.set(state=True, measIndex=m1)
positive_peak = mxo.measurement.result.actual.get(measIndex=m1)
print(f'\nMeasurement 1 Positive Peak = {value_to_si_string(positive_peak)}V.\n')

# Measurement 2 - peak min
m2 = repcap.MeasIndex.Nr2
mxo.measurement.source.set(signal_source=enums.SignalSource.C1, measIndex=m2)
mxo.measurement.main.set(meas_type=MeasType.MINimum, measIndex=m2)
mxo.measurement.enable.set(state=True, measIndex=m2)
negative_peak = mxo.measurement.result.actual.get(measIndex=m2)

print(f'\nMeasurement 2 Negative Peak = {value_to_si_string(negative_peak)}V.\n')

mxo.close()
