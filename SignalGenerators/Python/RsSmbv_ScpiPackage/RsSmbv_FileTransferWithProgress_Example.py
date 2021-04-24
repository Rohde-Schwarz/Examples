"""Example showing how you can transfer a big file to the instrument and from the instrument with showing the progress.
Since the SMBV100B is quite fast on data transfer, we slow it down by waiting for 100ms between each chunk transfer (1MB)
This way we see the transfer progress better and we do not need a file that is so big - let's take cca 20MB.
For big files, use the example without the time.sleep(0.1)"""

import time
import numpy as np
from RsSmbv import *


def my_transfer_handler(args):
    """Function called each time a chunk of data is transferred"""
    total_size = args.total_size if args.total_size is not None else "unknown"
    print(f"Context: '{args.context}{'with opc' if args.opc_sync else ''}', "
          f"chunk {args.chunk_ix}, "
          f"transferred {args.transferred_size} bytes, "
          f"total size {total_size}, "
          f"direction {'reading' if args.reading else 'writing'}, "
          f"data '{args.data}'")
    if args.end_of_transfer:
        print('End of Transfer')
    # Slow down the transfer by 200ms to see the progress better
    time.sleep(0.1)


RsSmbv.assert_minimum_version('4.80.2')
smbv = RsSmbv('TCPIP::10.112.1.73::HISLIP')
print(smbv.utilities.idn_string)
smbv.utilities.reset()

pc_file = r'c:\temp\bigFile.bin'
instr_file = '/var/user/bigFileInstr.bin'
pc_file_back = r'c:\temp\bigFileBack.bin'

# Generate a random file of 20MB size
x1mb = 1024 * 1024
with open(pc_file, 'wb') as file:
    for x in range(20):
        file.write(np.random.bytes(x1mb))

# Send the file to the instrument with events
smbv.events.on_write_handler = my_transfer_handler
smbv.utilities.data_chunk_size = x1mb
print(f'Sending file to the instrument...')
smbv.utilities.send_file_from_pc_to_instrument(pc_file, instr_file)
smbv.events.on_write_handler = None
print(f'Receiving file from the instrument...')
smbv.events.on_read_handler = my_transfer_handler
smbv.utilities.read_file_from_instrument_to_pc(instr_file, pc_file_back)
smbv.events.on_read_handler = None
smbv.close()
