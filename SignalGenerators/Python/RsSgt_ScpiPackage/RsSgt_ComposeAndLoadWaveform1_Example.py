"""The example:
 - creates waveform file from a csv-file with I/Q pairs
 - sends the file to the SGT100A instrument
 - activates the waveform
 You have the option of auto-scaling the samples to the full range with the parameter 'auto_scale'
 
 RsSgt documentation: https://rssgt.readthedocs.io/en/latest/
"""

import numpy as np
from RsSgt import *

RsSgt.assert_minimum_version('4.70.1')
sgt = RsSgt('TCPIP::192.168.1.100::hislip0')
print(sgt.utilities.idn_string)
sgt.utilities.reset()

pc_csv_file = r'c:\temp\arbFileExample.csv'
pc_wv_file = r'c:\temp\arbFileExample.wv'
instr_wv_file = '/var/user/InstrDemoFile.wv'

# Skip this part if you have a csv-file available

# Samples clock
clock_freq = 600e6
# wave clock
wave_freq = 120e6
# Scale factor - change it to less or more that 1 if you want to see the autoscaling capability of the create_waveform_file...() methods
scale_factor = 0.43
time_vector = np.arange(0, 50 / wave_freq, 1 / clock_freq)
# I-component an Q-component data
i_data = np.cos(2 * np.pi * wave_freq * time_vector) * scale_factor
q_data = np.sin(2 * np.pi * wave_freq * time_vector) * scale_factor

with open(pc_csv_file, 'w') as file:
    for x in range(len(i_data)):
        file.write(f'{i_data[x]},{q_data[x]}\n')

# Take that csv-file with the IQ-samples and create a wv file
result = sgt.arb_files.create_waveform_file_from_samples_file(pc_csv_file, pc_wv_file, clock_freq=100E6, auto_scale=False, comment='Created from a csv file')
print(result)

# Send to the instrument
sgt.arb_files.send_waveform_file_to_instrument(pc_wv_file, instr_wv_file)

# Selecting the waveform and load it in ARB
sgt.source.bb.arbitrary.waveform.set_select(instr_wv_file)

# Turning on the ARB baseband
sgt.source.bb.arbitrary.set_state(True)

# Turning on the RF output state state
sgt.output.state.set_value(True)

sgt.close()
