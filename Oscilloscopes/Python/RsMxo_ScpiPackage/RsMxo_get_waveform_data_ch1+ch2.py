"""
Getting started - how to work with RsMxo Python package.
This example performs the following actions on an MXO Oscilloscope:
- Basic configuration
- Triggers an acquisition and waits for it to finish.
- Fetches the waveforms for channel 1 and 2, and paints them into a plot.

The example also shows the corresponding SCPI commands next to the RsMxo calls.
Notice that the python RsMxo interfaces track the SCPI commands structure.
Additionally, the SCPI communication logger into the console shows you the SCPI communication with your MXO.
"""

from RsMxo import *
from RsMxo.enums import *
import matplotlib.pyplot as plt

RsMxo.assert_minimum_version('2.6.4')

# Open the session - adjust the resource name to fit your instrument
mxo = RsMxo('TCPIP::localhost::hislip0', id_query=False)
# Greetings, stranger...
print(f'Hello, I am: {mxo.utilities.idn_string}')

# Print commands to the console with the logger
mxo.utilities.logger.mode = LoggingMode.On
mxo.utilities.logger.log_to_console = True

#   SYSTem:DISPlay:UPDate ON
mxo.system.display.set_update(True)

#   TRIGger:MODE AUTO
mxo.trigger.set_mode(trigger_mode=TriggerMode.AUTO)
mxo.trigger.event.source.set(source_detailed=TriggerSource.C1)

#   ACQuire:SRATe:MODE AUTO
mxo.acquire.symbolRate.set_mode(sample_rate_mode=AutoManualMode.AUTO)

# Create 'Channel' object 'ch1', that always addresses the Analog Channel 1
ch1 = mxo.channel.clone()
ch1.repcap_channel_set(channel=repcap.Channel.Ch1)

# Create 'Channel' object 'ch2', that always addresses the Analog Channel 2
ch2 = mxo.channel.clone()
ch2.repcap_channel_set(channel=repcap.Channel.Ch2)

# CHANnel1:STATe ON
ch1.state.set(True)

# CHANnel2:STATe ON
ch2.state.set(True)

# Perform the acquisition, wait for it to finish.
# RUNSingle;*OPC
mxo.run.single_and_wait()

#         CHANnel1:DATA:HEADer?
data_hdr_ch1 = ch1.data.header.get()
print(f'Channel 1 data: header:\n'
	  f'Time Start: {data_hdr_ch1.Xstart}\n'
	  f'Time Stop: {data_hdr_ch1.Xstop}\n'
	  f'Record Length: {data_hdr_ch1.Record_Length}\n'
	  f'Values per Sample: {data_hdr_ch1.Vals_Per_Smp}')

#   CHANnel1:DATA:VALues?
wform1 = ch1.data.values.get()
plt.plot(wform1)

#         CHANnel2:DATA:HEADer?
data_hdr_ch2 = ch2.data.header.get()
print(f'Channel 2 data: header:\n'
	  f'Time Start: {data_hdr_ch2.Xstart}\n'
	  f'Time Stop: {data_hdr_ch2.Xstop}\n'
	  f'Record Length: {data_hdr_ch2.Record_Length}\n'
	  f'Values per Sample: {data_hdr_ch2.Vals_Per_Smp}')

#   CHANnel2:DATA:VALues?
wform2 = ch2.data.values.get()
plt.plot(wform2)

plt.legend(['CH1', 'CH2'])
plt.xlabel("Samples")
plt.ylabel("Amplitude in Volts")

plt.show()

mxo.close()
