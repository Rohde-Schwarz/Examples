"""The example:
 - creates waveform file from two i_data and q_data vectors
 - sends the file to the SMW instrument
 - activates the waveform on Output A
 - creates waveform file from those same two vectors, but i_data is swapped for q_data
 - activates the waveform on Output B
 You have the option of auto-scaling the samples to the full range
 The example auto-scales the Output B signal, the Output A signal is left as generated
"""

import numpy as np

from RsSmw import *

RsSmw.assert_minimum_version('4.80.2')
smw = RsSmw('TCPIP::10.112.1.179::HISLIP')
print(smw.utilities.idn_string)
smw.utilities.reset()

pc_wv_file = r'c:\temp\arbFileExample.wv'
instr_wv_file_outA = '/var/user/InstrDemoFile_outA.wv'
instr_wv_file_outB = '/var/user/InstrDemoFile_outB.wv'

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

# Take those samples and create a wv file, send it to the instrument with the name instr_wv_file_outA (not auto-scaled)
result = smw.arb_files.create_waveform_file_from_samples(i_data, q_data, pc_wv_file, clock_freq=100E6, auto_scale=False, comment='Created from I/Q vectors')
smw.arb_files.send_waveform_file_to_instrument(pc_wv_file, instr_wv_file_outA)
# Take those swapped samples and create another wv file, send it to the instrument with the name instr_wv_file_outB (auto-scaled to full range)
result = smw.arb_files.create_waveform_file_from_samples(q_data, i_data, pc_wv_file, clock_freq=100E6, auto_scale=True, comment='Created from swapped Q/I vectors')
smw.arb_files.send_waveform_file_to_instrument(pc_wv_file, instr_wv_file_outB)

# Selecting the waveform and load it in ARB for Output A
smw.source.bb.arbitrary.waveform.set_select(instr_wv_file_outA)
smw.source.frequency.set_frequency(1.1E9)
smw.source.power.level.immediate.set_amplitude(-11.1)
# Turning on the ARB baseband A
smw.source.bb.arbitrary.set_state(True)
# Turning on the state of RF-A
smw.output.state.set_value(True)

# Creating a clone for Output B
smwB = smw.clone()
smwB.repcap_hwInstance_set(repcap.HwInstance.InstB)

# Selecting the waveform and load it in ARB for Output B
smwB.source.bb.arbitrary.waveform.set_select(instr_wv_file_outB)
smwB.source.frequency.set_frequency(2.2E9)
smwB.source.power.level.immediate.set_amplitude(-22.2)
# Turning on the ARB baseband B
smwB.source.bb.arbitrary.set_state(True)
# Turning on the state of RF-B
smwB.output.state.set_value(True)

smw.close()
