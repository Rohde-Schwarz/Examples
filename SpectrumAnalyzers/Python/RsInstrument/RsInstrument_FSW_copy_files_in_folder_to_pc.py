# GitHub examples repository path: SpectrumAnalyzers/Python/RsInstrument
# Example for FSW / FSV / FSVA / FPS Spectrum Analyzers
# to copy all the files of one folder instrument (not recursively!!!) to your control PC.
# Preconditions:
# - Installed RsInstrument Python module 1.70+ from pypi.org
# - Installed VISA e.g. R&S Visa 5.12.x or newer

import os
from RsInstrument import *  # The RsInstrument package is hosted on pypi.org, see Readme.txt for more details
from time import time
from random import random

instr_dir = 'C:/R_S/instr/user' # Adjust this path to fit your instrument
pc_dir = 'c:/temp/copy_temp'

fsw = None
RsInstrument.assert_minimum_version('1.70.0')
try:
	# Adjust the VISA Resource string to fit your instrument
	fsw = RsInstrument('TCPIP::localhost::INSTR', True, False, options='SelectVisa=ni')
	fsw.visa_timeout = 1500  # Timeout for VISA Read Operations
	fsw.instrument_status_checking = True  # Error check after each command
except Exception as ex:
	print('Error initializing the instrument session:\n' + ex.args[0])
	exit()

print(f'Driver Version: {fsw.driver_version}')
print(f'SpecAn IDN: {fsw.idn_string}')
print(f'SpecAn Options: {",".join(fsw.instrument_options)}')

# change the current instrument directory to our desired one
if not os.path.exists(pc_dir):
	os.makedirs(pc_dir)
fsw.write(f"MMEMory:CDIRectory '{instr_dir}'")
items = [x.strip('"') for x in fsw.query_str_list("MMEMory:CATalog:LONG?")]
items_plain = fsw.query_str("MMEMory:CATalog:LONG?")
items.pop(0)
items.pop(0)
resh_items = [items[i:i+3] for i in range(0, len(items), 3)]

files = list(filter(lambda x: x[1] != 'DIR', resh_items))
uq_files = []
[uq_files.append(item) for item in files if item not in uq_files]

folders = list(filter(lambda x: x[1] == 'DIR', resh_items))
uq_folders = []
[uq_folders.append(item) for item in folders if item not in uq_folders]

print(f'Files count: {len(uq_files)}')
print(f'Folders count: {len(uq_folders)}')

i = 1
for el in uq_files:
	print(f'File {i} / {len(files)}: {el[0]}, size {el[2]} bytes, copying ...', end='')
	instr_file = instr_dir + '/' + el[0] + ("aa" if random() > 0.65 else '')
	pc_file = pc_dir + '/' + el[0]
	# We put a error guard here to isolate each file copy exception
	with fsw.visa_tout_suppressor() as supp:
		fsw.clear_status()
		fsw.read_file_from_instrument_to_pc(instr_file, pc_file)
	if supp.get_timeout_occurred():
		print('ERROR')
	else:
		print('OK')
	i+=1

# Close the session
fsw.close()
