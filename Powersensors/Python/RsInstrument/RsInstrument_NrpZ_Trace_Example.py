# GitHub examples repository path: Powersensors/Python/RsInstrument

# Example for NRP-Z powersensors
# Preconditions:
# - Installed RsInstrument Python module from pypi.org
# - Installed R&S Visa 5.12.x or newer

from RsInstrument import *  # The RsInstrument package is hosted on pypi.org, see Readme.txt for more details
import time

nrpz = None
# Make sure you have the last version of the RsInstrument
RsInstrument.assert_minimum_version('1.22.0')
try:
	# -----------------------------------------------------------
	# Initialization:
	# -----------------------------------------------------------
	# Adjust the VISA Resource string to fit your instrument
	nrpz = RsInstrument('RSNRP::0x0095::104015::INSTR', True, False)
	nrpz.visa_timeout = 3000  # Timeout for VISA Read Operations
	nrpz.instrument_status_checking = True  # Error check after each command
except Exception as ex:
	print('Error initializing the instrument session:\n' + ex.args[0])
	exit()

print(f'Visa manufacturer: {nrpz.visa_manufacturer}')
print(f'Instrument Identification string: {nrpz.idn_string}')

nrpz.write_str("*RST")  # Reset the instrument, clear the Error queue
nrpz.write_str("INIT:CONT OFF")  # Switch OFF the continuous sweep
# -----------------------------------------------------------
# Basic Settings:
# -----------------------------------------------------------
nrpz.write_str('INIT:CONT OFF')
nrpz.write_str('SENS:FUNC \"XTIM:POW\"')
nrpz.write_str('SENS:TRAC:POIN 8191')
nrpz.write_str('SENS:TRAC:TIME 20.0e-3')
nrpz.write_str('SENS:AVER:COUN:AUTO OFF')
nrpz.write_str('SENS:AVER:COUN 2')
nrpz.write_str('SENS:AVER:STAT ON')
nrpz.write_str('TRIG:SOUR IMM')
nrpz.write_str('TRIG:LEV 100e-6')
nrpz.write_str('TRIG:DEL -5.0e-6')
# -----------------------------------------------------------
# SyncPoint 'SettingsApplied' - all the settings were applied
# -----------------------------------------------------------
nrpz.write_str("INIT:IMM")  # Start the sweep

success = False
for x in range(0, 200):
	status = nrpz.query_int('STAT:OPER:COND?')
	if (status & 16) == 0:
		# Status register bit 4 signals MEASURING status
		# Finished measuring, break
		success = True
		break
	time.sleep(0.02)

if not success:
	raise TimeoutError("Measurement timed out")

# -----------------------------------------------------------
# Fetching the results, format does not matter, the driver function always parses it correctly
# -----------------------------------------------------------
nrpz.write_str('FORMAT ASCII')
results = nrpz.query_str('FETCH?').split(',')
print(f'Measured samples #{len(results)}\nValues:\n{results}')

# Close the session
nrpz.close()
