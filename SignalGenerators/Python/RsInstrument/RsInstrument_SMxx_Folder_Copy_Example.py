# GitHub examples repository path: SignalGenerators/Python/RsInstrument
# Example for SMxx Signal Generators shows how to copy all files from the instrument's folder (non-recursive)
# to the folder in your control PC.
# Preconditions:
# - Installed RsInstrument Python module from pypi.org
# - Installed VISA e.g. R&S Visa 5.12.x or newer
#
# RsInstrument documentation: https://rsinstrument.readthedocs.io/en/latest/

from RsInstrument import *  # The RsInstrument package is hosted on pypi.org, see Readme.txt for more details
import numpy as np
import os
import shutil

smw = None
RsInstrument.assert_minimum_version('1.54.0')
try:
	# Adjust the VISA Resource string to fit your instrument
	smw = RsInstrument('TCPIP::192.168.1.100::hislip0')
except Exception as ex:
	print('Error initializing the instrument session:\n' + ex.args[0])
	exit()

print(f'Driver Version: {smw.driver_version}')
print(f'IDN: {smw.idn_string}')
print(f'Options: {",".join(smw.instrument_options)}')

root_folder = '/var/user'
# get all the items in the instrument's folder /var/user
catalog = smw.query_str_list(f"MMEM:CAT? '{root_folder}'")
# delete first two entries, and reshape the list to listOfLists
catalog.pop(1)
catalog.pop(0)
catalog = list(map(lambda x: x.strip('"\''), catalog))
items = np.array(catalog).reshape(-1, 3).tolist()
# Split to folders and files
folders = list(map(lambda els: els[0], list(filter(lambda x: x[1] == 'DIR', items))))
files = list(map(lambda els: els[0], list(filter(lambda x: x[1] != 'DIR', items))))

print("\nSub-Folders:")
for folder in folders:
	print(folder)

print("\nFiles:")
for file in files:
	print(file)

target_pc_folder = r'c:/temp/_instrument'
# Remove the directory and recreate it
if not os.path.exists(target_pc_folder):

	os.makedirs(target_pc_folder)
else:
	# Delete it and recreate
	shutil.rmtree(target_pc_folder)
	os.makedirs(target_pc_folder)

# Read all the files to the PC folder, path 'c:/temp/_instrument'
print()
for file in files:
	print("Copying file: " + file)
	smw.read_file_from_instrument_to_pc(root_folder + '/' + file, target_pc_file=target_pc_folder + '/' + file)

# Close the session
smw.close()