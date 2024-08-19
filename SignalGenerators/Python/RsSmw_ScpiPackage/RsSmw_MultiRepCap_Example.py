"""
This example shows how to work with commands that have many repeated capabilities (numeric suffixes).
The example does not demonstrate any valid instrument settings, rather the instrument driver general rules of working with the repeated capabilities.

RsSmw documentation: https://rohde-schwarz.github.io/RsSmw_PythonDocumentation/index.html
"""

from RsSmw import *

RsSmw.assert_minimum_version('5.0.44')
smw = RsSmw('TCPIP::192.168.1.100::hislip0', True, True)
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
# sending SOURce1:BB:NR5G:SCHed:CELL1:SUBF3:USER0:BWPart1:ALLoc0:APMap:COL0:ROW3:IMAGinary 10.0
smw.source.bb.nr5G.scheduling.cell.subf.user.bwPart.alloc.apMap.col.row.imaginary.set(10.0, repcap.CellNull.Nr1, repcap.SubframeNull.Nr3, repcap.UserNull.Nr0, repcap.BwPartNull.Nr1, repcap.AllocationNull.Nr0, repcap.ColumnNull.Nr0, repcap.RowNull.Nr3)

# Option 2: only some arguments with keywords, others keep their default values:
# sending SOURce1:BB:NR5G:SCHed:CELL1:SUBF3:USER0:BWPart1:ALLoc0:APMap:COL0:ROW3:IMAGinary 10.0
# Default values for skipped repCaps:
# - repcap.UserNull.Nr0
# - repcap.Allocation.Nr0
# - repcap.ColumnNull.Nr0
smw.source.bb.nr5G.scheduling.cell.subf.user.bwPart.alloc.apMap.col.row.imaginary.set(10.0, cellNull=repcap.CellNull.Nr1, subframeNull=repcap.SubframeNull.Nr3, bwPartNull=repcap.BwPartNull.Nr1, rowNull=repcap.RowNull.Nr3)

# Option 3: default values are set in the group interfaces, and then left to default in the method call:
smw.source.bb.nr5G.scheduling.cell.repcap_cellNull_set(repcap.CellNull.Nr1)
smw.source.bb.nr5G.scheduling.cell.subf.repcap_subframeNull_set(repcap.SubframeNull.Nr3)
smw.source.bb.nr5G.scheduling.cell.subf.user.repcap_userNull_set(repcap.UserNull.Nr0)
smw.source.bb.nr5G.scheduling.cell.subf.user.bwPart.repcap_bwPartNull_set(repcap.BwPartNull.Nr1)
smw.source.bb.nr5G.scheduling.cell.subf.user.bwPart.alloc.repcap_allocationNull_set(repcap.AllocationNull.Nr0)
smw.source.bb.nr5G.scheduling.cell.subf.user.bwPart.alloc.apMap.col.repcap_columnNull_set(repcap.ColumnNull.Nr0)
smw.source.bb.nr5G.scheduling.cell.subf.user.bwPart.alloc.apMap.col.row.repcap_rowNull_set(repcap.RowNull.Nr3)
# and then just use the set() method without repeated capabilities:
# sending SOURce1:BB:NR5G:SCHed:CELL1:SUBF3:USER0:BWPart1:ALLoc0:APMap:COL0:ROW3:IMAGinary 10.0
smw.source.bb.nr5G.scheduling.cell.subf.user.bwPart.alloc.apMap.col.row.imaginary.set(10.0)

# We can clone the cell interface and change the default cell from Nr1 to Nr2 without affecting the origin interface:
cell_nr2 = smw.source.bb.nr5G.scheduling.cell.clone()
cell_nr2.repcap_cellNull_set(repcap.CellNull.Nr2)

# Now we have an independent object cell_nr2, and can set the same command for cell Nr2
# All other repcap default values are the same:
# repcap.SubframeNull.Nr3
# repcap.ColumnNull.Nr2
# repcap.RowNull.Nr3
# sending SOURce1:BB:NR5G:SCHed:CELL2:SUBF3:USER:BWPart:ALLoc:APMap:COL2:ROW3:IMAGinary 10.0
cell_nr2.subf.user.bwPart.alloc.apMap.col.row.imaginary.set(10.0)

# Option 4: Combination of Options 1, 2 and 3 - we use the default values from the group interfaces and explicitly define some of them:
# Here we change the channel to 5 and Column to 4, all others are default from the group
# sending SOURce1:BB:NR5G:SCHed:CELL5:SUBF3:USER:BWPart:ALLoc:APMap:COL4:ROW3:IMAGinary 10.0
smw.source.bb.nr5G.scheduling.cell.subf.user.bwPart.alloc.apMap.col.row.imaginary.set(10.0, cellNull=repcap.CellNull.Nr5, columnNull=repcap.ColumnNull.Nr4)

smw.close()
