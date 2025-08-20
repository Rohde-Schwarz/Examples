"""
This example makes a screenshot of the current screen content of an MXO Oscilloscope display,
and transfers it into the host PC.
"""

from RsMxo import *
from RsMxo.enums import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

pc_file_name = 'screenshot.png'

RsMxo.assert_minimum_version('2.6.2')

# Open the session - adjust the resource name to fit your instrument
mxo = RsMxo('TCPIP::10.103.34.12::hislip0', id_query=False)
# Greetings, stranger...
print(f'Hello, I am: {mxo.utilities.idn_string}')

mxo.system.display.set_update(True)

mxo.hardCopy.set_destination(medium=PrintTarget.MMEM)
mxo.hardCopy.device.set_language(PictureFileFormat.PNG)

mxo.hardCopy.immediate.perform()
file_content = mxo.hardCopy.get_data()
with open(pc_file_name, 'wb') as screenshot:
    screenshot.write(file_content)
print(f'Screenshot file saved to "{pc_file_name}"')

mxo.close()

# Show the screenshot picture
img = mpimg.imread(pc_file_name)
plt.imshow(img)
plt.show()

