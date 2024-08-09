"""The example:
 - creates waveform file from two i_data and q_data vectors
 - sends the file to the SMBV instrument
 - activates the waveform
 You have the option of auto-scaling the samples to the full range with the parameter 'auto_scale'
"""

import numpy as np
from RsSmbv import *

RsSmbv.assert_minimum_version('4.80.2')
smbv = RsSmbv('TCPIP::192.168.1.100::hislip0')
print(smbv.utilities.idn_string)
smbv.utilities.reset()

pc_wv_file = r'c:\temp\arbFileExample.wv'
instr_wv_file = '/var/user/InstrDemoFile.wv'

# Creating the I/Q vectors as lists: i_data / q_data
# Samples clock
clock_freq = 100e6
# wave clock
wave_freq = 25e6
# Scale factor - change it to less or more that 1 if you want to see the autoscaling capability of the create_waveform_file...() methods
scale_factor = 0.8

samples_count = 200
time_step = 1 / clock_freq
time_vector = [x * time_step for x in range(samples_count)]
# I-component an Q-component data
i_data = [np.cos(2 * np.pi * wave_freq * tv) * scale_factor for tv in time_vector]
q_data = [np.sin(2 * np.pi * wave_freq * tv) * scale_factor for tv in time_vector]

# Take those samples and create a wv file, send it to the instrument with the name instr_wv_file (not auto-scaled)
result = smbv.arb_files.create_waveform_file_from_samples(i_data, q_data, pc_wv_file, clock_freq=clock_freq, auto_scale=False, comment='Created from I/Q vectors')
smbv.arb_files.send_waveform_file_to_instrument(pc_wv_file, instr_wv_file)

# Selecting the waveform and load it in the ARB
smbv.source.bb.arbitrary.waveform.set_select(instr_wv_file)
smbv.source.frequency.set_frequency(1.1E9)
smbv.source.power.level.immediate.set_amplitude(-11.1)
# Turning on the ARB baseband
smbv.source.bb.arbitrary.set_state(True)
# Turning on the RF out state
smbv.output.state.set_value(True)

smbv.close()
