"""
This example makes a screenshot of the current screen content of an RTO Oscilloscope display,
and transfers it into the host PC.
"""
import os
from pathlib import Path

from rsrtx import *
from rsrtx.enums import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

pc_file_name = 'screenshot_pc.png'
instr_file_name = 'screenshot_instr.png'

RsRtx.assert_minimum_version('5.55.0')

# Open the session - adjust the resource name to fit your instrument
rto = RsRtx('TCPIP::10.103.34.49::hislip0')
# Greetings, stranger...
print(f'Hello, I am: {rto.utilities.idn_string}')
rto.utilities.visa_timeout = 5000

rto.system.display.set_update(True)

rto.hardCopy.set_destination(medium='MMEM')
rto.hardCopy.device.set_language(PictureFileFormat.PNG)
current_dir = rto.massMemory.get_current_directory()
instr_file_path = current_dir + '\\' + instr_file_name
rto.massMemory.set_name(instr_file_path)

rto.hardCopy.immediate.perform()

file_content = rto.utilities.read_file_from_instrument_to_pc(instr_file_path, pc_file_name)
full_instr_file_path = Path(__file__).resolve().with_name(instr_file_name)
print(f'Screenshot file saved to "{pc_file_name}". Full Path: "{full_instr_file_path}"')

rto.close()

# Show the screenshot picture
img = mpimg.imread(pc_file_name)
plt.imshow(img)
plt.show()

