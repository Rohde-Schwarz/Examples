# This example shows how to work with commands that have many repeated capabilities (numeric suffixes)
# The example does not demonstrate any valid instrument settings, rather the instrument driver general rules of working with the repeated capabilities

from RsSmw import *

smw = RsSmw('TCPIP::10.112.1.179::HISLIP', True, True)
print(f'Driver Info: {smw.utilities.driver_version}')
print(f'Instrument: {smw.utilities.idn_string}')

# The smw object addresses the RF Output A - SCPI command header 'SOURCE1'
smw.repcap_hwInstance_set(repcap.HwInstance.InstA)

# Switching the error checking off to avoid errors from invalid parameter settings
smw.utilities.instrument_status_checking = False

smw.source.bb.nr5G.set_state(True)

# Setting commands with many repeated capabilities:
# [SOURce<HW>]:BB:NR5G:SCHed:CELL<CH>:SUBF<ST>:USER:BWPart:ALLoc:APMap:COL<S2US>:ROW<S3US>:IMAGinary

# Option 1: explicit definition:
# sending SOURce1:BB:NR5G:SCHed:CELL1:SUBF3:USER:BWPart:ALLoc:APMap:COL2:ROW3:IMAGinary 10.0
smw.source.bb.nr5G.scheduling.cell.subf.user.bwPart.alloc.apMap.col.row.imaginary.set(10.0, repcap.Channel.Nr1, repcap.Stream.Nr3, repcap.Column.Nr2, repcap.Row.Nr3)

# Option 2: arguments with keywords:
smw.source.bb.nr5G.scheduling.cell.subf.user.bwPart.alloc.apMap.col.row.imaginary.set(10.0, stream=repcap.Stream.Nr3, row=repcap.Row.Nr3)

# Option 3: default values are set in the group interfaces, and then left to default in the method call:
smw.source.bb.nr5G.scheduling.cell.repcap_channel_set(repcap.Channel.Nr1)
smw.source.bb.nr5G.scheduling.cell.subf.repcap_stream_set(repcap.Stream.Nr3)
smw.source.bb.nr5G.scheduling.cell.subf.user.bwPart.alloc.apMap.col.repcap_column_set(repcap.Column.Nr2)
smw.source.bb.nr5G.scheduling.cell.subf.user.bwPart.alloc.apMap.col.row.repcap_row_set(repcap.Row.Nr3)
# and then just use the set() method without repeated capabilities:
# sending SOURce1:BB:NR5G:SCHed:CELL1:SUBF3:USER:BWPart:ALLoc:APMap:COL2:ROW3:IMAGinary 10.0
smw.source.bb.nr5G.scheduling.cell.subf.user.bwPart.alloc.apMap.col.row.imaginary.set(10.0)

# We can clone the cell interface and change the default channel from Nr1 to Nr2 without affecting the original source cell interface:
cell_nr2 = smw.source.bb.nr5G.scheduling.cell.clone()
cell_nr2.repcap_channel_set(repcap.Channel.Nr2)

# Now we have an independent object cell_nr2, and can set the same command for channel Nr2
# All other repcap default values are the same:
# repcap.Stream.Nr3
# repcap.Column.Nr2
# repcap.Row.Nr3
# sending SOURce1:BB:NR5G:SCHed:CELL2:SUBF3:USER:BWPart:ALLoc:APMap:COL2:ROW3:IMAGinary 10.0
cell_nr2.subf.user.bwPart.alloc.apMap.col.row.imaginary.set(10.0)

# Option 4: Combination of Options 1, 2 and 3 - we use the default values from the group interfaces and explicitly define some of them:
# Here we change the channel to 5 and Column to 4, all others are default from the group
# sending SOURce1:BB:NR5G:SCHed:CELL5:SUBF3:USER:BWPart:ALLoc:APMap:COL4:ROW3:IMAGinary 10.0
smw.source.bb.nr5G.scheduling.cell.subf.user.bwPart.alloc.apMap.col.row.imaginary.set(10.0, repcap.Channel.Nr5, column=repcap.Column.Nr4)

smw.close()
