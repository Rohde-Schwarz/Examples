"""
Getting started - how to work with rsrtx Python package.
This example performs the following actions on an RTO Oscilloscope:
- Basic configuration
- Triggers an acquisition and waits for it to finish.
- Fetches the waveforms for channel 1 and paints it into a plot.

The example also shows the corresponding SCPI commands next to the rsrtx calls.
Notice that the python rsrtx interfaces track the SCPI commands structure.
Additionally, the SCPI communication logger into the console shows you the SCPI communication with your RTO.
"""

from rsrtx import *
from rsrtx.enums import *
import matplotlib.pyplot as plt

RsRtx.assert_minimum_version('5.55.0')

# Open the session - adjust the resource name to fit your instrument
rto = RsRtx('TCPIP::10.103.34.49::hislip0')
# Greetings, stranger...
print(f'Hello, I am: {rto.utilities.idn_string}')

# Print commands to the console with the logger
rto.utilities.logger.mode = LoggingMode.On
rto.utilities.logger.log_to_console = True

#   SYSTem:DISPlay:UPDate ON
rto.system.display.set_update(True)

#   TRIGger:MODE AUTO
rto.trigger.mode.set(trigger_mode=TriggerMode.AUTO)

#   TRIGger:EVENT:EVENT SINGle
rto.trigger.event.event.set(class_py=TriggerEventClass.SINGle)

#   ACQuire:SRATe:MODE AUTO
rto.acquire.set_symbol_rate(sample_rate=20000000000)

# Create 'Channel' object 'ch1', that always addresses the Analog Channel 1
ch1 = rto.channel.clone()
ch1.repcap_channel_set(channel=repcap.Channel.Ch1)

# CHANnel1:STATe ON
ch1.state.set(True)

# Perform the acquisition, wait for it to finish.
#   RUNSingle;*OPC
rto.run.single_and_wait()

#         CHANnel1:WAVEFORM1:DATA:HEADer?
data_hdr_ch1 = ch1.waveform.data.header.get()
print(f'Channel 1 data: header:\n'
	  f'Time Start: {data_hdr_ch1.Start}\n'
	  f'Time Stop: {data_hdr_ch1.Stop}\n'
	  f'Record Length: {data_hdr_ch1.Record_Length}\n'
	  f'Values per Sample: {data_hdr_ch1.Vals_Per_Smp}')

#   CHANnel1:WAVEFORM1:DATA:VALues?
wform1 = ch1.waveform.data.values.get()
plt.plot(wform1)

plt.legend(['CH1'])
plt.xlabel("Samples")
plt.ylabel("Amplitude in Volts")

plt.show()

rto.close()
