"""
Getting started - how to work with RsMxo Python package.
This example performs basic settings on an MXO oscilloscope.
It shows the RsMxo calls and their corresponding SCPI commands.
Notice that the python RsMxo interfaces track the SCPI commands syntax.

RsMxo documentation:
"""

from RsMxo import *
from RsMxo.enums import TriggerMode, AutoManualMode

# Open the session
mxo = RsMxo('TCPIP::10.212.0.74::hislip0', id_query=False)
# Greetings, stranger...
print(f'Hello, I am: {mxo.utilities.idn_string}')

# Print commands to the console with the logger
mxo.utilities.logger.mode = LoggingMode.On
mxo.utilities.logger.log_to_console = True

mxo.system.display.set_update(True)
mxo.trigger.set_mode(trigger_mode=TriggerMode.AUTO)
mxo.acquire.symbolRate.set_mode(sample_rate_mode=AutoManualMode.AUTO)

# Create 'Channel' object 'ch1', that always addresses the Analog Channel 1
ch1 = mxo.channel.clone()
ch1.repcap_channel_set(channel=repcap.Channel.Ch1)

# Create 'Channel' object 'ch2', that always addresses the Analog Channel 2
ch2 = mxo.channel.clone()
ch2.repcap_channel_set(channel=repcap.Channel.Ch2)

ch1.state.set(True)
ch2.state.set(True)

mxo.runSingle.set()

data1 = ch1.waveform.data.values.get()
data2 = ch2.waveform.data.values.get()
