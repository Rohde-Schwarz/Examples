"""The example:
 - creates waveform file from two i_data and q_data vectors
 - sends the file to the SGT100A instrument
 - activates the waveform
 You have the option of auto-scaling the samples to the full range with the parameter 'auto_scale'
"""

import numpy as np
from RsSgt import *

RsSgt.assert_minimum_version('4.70.1')
sgt = RsSgt('TCPIP::10.214.1.57::HISLIP')
print(sgt.utilities.idn_string)
sgt.utilities.reset()

pc_wv_file = r'c:\temp\arbFileExample.wv'
instr_wv_file = '/var/user/InstrDemoFile.wv'

# Creating the I/Q vectors as lists: i_data / q_data
# Samples clock
clock_freq = 600e6
# wave clock
wave_freq = 120e6
# Scale factor - change it to less or more that 1 if you want to see the autoscaling capability of the create_waveform_file...() methods
scale_factor = 0.8
time_vector = np.arange(0, 50 / wave_freq, 1 / clock_freq)
# I-component an Q-component data
i_data = np.cos(2 * np.pi * wave_freq * time_vector) * scale_factor
q_data = np.sin(2 * np.pi * wave_freq * time_vector) * scale_factor

# Take those samples and create a wv file, send it to the instrument with the name instr_wv_file (not auto-scaled)
result = sgt.arb_files.create_waveform_file_from_samples(i_data, q_data, pc_wv_file, clock_freq=100E6, auto_scale=False, comment='Created from I/Q vectors')
sgt.arb_files.send_waveform_file_to_instrument(pc_wv_file, instr_wv_file)

# Selecting the waveform and load it in the ARB
sgt.source.bb.arbitrary.waveform.set_select(instr_wv_file)
sgt.source.frequency.fixed.set_value(1.1E9)
sgt.source.power.level.immediate.set_amplitude(-11.1)
# Turning on the ARB baseband
sgt.source.bb.arbitrary.set_state(True)
# Turning on the RF out state
sgt.output.state.set_value(True)

sgt.close()
