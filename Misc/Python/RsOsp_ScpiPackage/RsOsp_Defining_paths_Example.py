"""This is a RsOsp example for communicating with your OSPxxx instrument.
It shows how to use the RsOsp interface by showing the composed SCPI commands.
The example defines one path in different ways and at the end closes the path.
The example assumes that the OSP has 2 installed options B101 on M01 and B102 on M02.
"""

# RsOsp package is hosted on pypi.org
from RsOsp import *

# Initialize the session
osp = RsOsp('TCPIP::192.168.2.101::hislip0')

osp.utilities.reset()
print(f"\nHello, I am: '{osp.utilities.idn_string}'")
print(f'Instrument installed options: {",".join(osp.utilities.instrument_options)}')

# All the following commands do the same:

# Direct SCPI write method is still available:
# Pathname: PATH_A / F01M02(0501) => F01: Frame 1 (first OSP) / M02: Module 2 / 05: Switch Position 5 / 01: Relay ID on Module: 1
osp.utilities.write('ROUTe:PATH:DEFine "PATH_A", (@F01M01(0001),F01M01(0102),F01M02(0501),F01M02(0602))')

# Universal DEFINE method:
# SCPI sent is the same as above: 'ROUTe:PATH:DEFine "PATH_A",(@F01M01(0001),F01M01(0102),F01M02(0501),F01M02(0602))'
osp.route.path.define.set('PATH_A', '(@F01M01(0001),F01M01(0102),F01M02(0501),F01M02(0602))')

# Method for defining multiple channels - no need to use the '@' and the most-outer round brackets:
# SCPI sent is the same as above: 'ROUTe:PATH:DEFine "PATH_A",(@F01M01(0001),F01M01(0102),F01M02(0501),F01M02(0602))'
osp.route.path.define.set_multiple_channels('PATH_A', [ 'F01M01(0001)', 'F01M01(0102)', 'F01M02(0501)', 'F01M02(0602)' ])

# This method defines a single channel - no need to use the '@' and the most-outer round brackets:
# SCPI sent is similar as the one above: 'ROUTe:PATH:DEFine "PATH_A",(F01M02(0501))'
osp.route.path.define.set_single_channel('PATH_A', 'F01M02(0501)')

# Print list of all defined paths
# SCPI sent: SCPI: ROUTe:PATH:CATalog?
paths = osp.route.path.get_catalog()
print('Defined paths:\n' + '\n'.join(paths))

# Close the defined path
osp.route.close.set_path('PATH_A')

# Close the session
osp.close()
