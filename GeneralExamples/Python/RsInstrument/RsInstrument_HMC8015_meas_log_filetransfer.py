"""
Created on 2020/10

Author: Jahns_P
Version Number: 3
Date of last change: 2020/10/08
Requires: HMC8015, FW 1.403 or newer and adequate options
- Installed RsInstrument Python module 1.7.0.37 or newer
- Installed VISA e.g. R&S Visa 5.12.x or newer

Description: Setup measurement and log to a file for a certain time, transfer the log file to the PC


General Information:

Please allways check this example script for unsuitable setting that may
destroy your DUT befor connecting it to the instrument!
This example does not claim to be complete. All information has been
compiled with care. However errors can not be ruled out. 

Please find more information about RsInstrument at 
https://rsinstrument.readthedocs.io/en/latest/
"""

# --> Import necessary packets  
from RsInstrument import *
from time import sleep

# Define variables
ressource = 'TCPIP::10.205.0.21::5025::SOCKET'  # VISA resource string for the device
x = 1  # For counters
y = 1  # For counters also
intdurtime = "15"  # Integrator duration time in seconds
loopResponse = "1"  # Variable for diverse loop requests
Response = "0"  # Variable for diverse requests
pagenum = 1  # Number of the display page to be logged
logdur = 2  # Log time in seconds
log_file_name = 'LOG1234.CSV'  # Name of the log file

# Define the device handle
RsInstrument.assert_minimum_version('1.15.0.68')
HMC8015 = RsInstrument(ressource, True, True, "SelectVisa='rs'")
"""
(ressource, True, True, "SelectVisa='rs'") has the following meaning:
(VISA-resource, id_query, reset, options)
- id_query: if True: the instrument's model name is verified against the models 
supported by the driver and eventually throws an exception.   
- reset: Resets the instrument (sends *RST) command and clears its status syb-system
- option SelectVisa:
			'SelectVisa = 'socket' - uses no VISA implementation for socket connections - you do not need any VISA-C installation
			'SelectVisa = 'rs' - forces usage of Rohde&Schwarz Visa
			'SelectVisa = 'ni' - forces usage of National Instruments Visa     
"""


# ----------------- Define subroutines for error and command completion requests -----------------
def comprep():
	"""Preparation of the communication (termination, etc...)"""
	print(f'VISA Manufacturer: {HMC8015.visa_manufacturer}')  # Confirm VISA package to be choosen
	HMC8015.visa_timeout = 5000  # Timeout for VISA Read Operations
	HMC8015.opc_timeout = 3000  # Timeout for opc-synchronised operations
	HMC8015.instrument_status_checking = True  # Error check after each command
	HMC8015.clear_status()  # Clear status register


def close():
	"""Close the VISA session"""
	HMC8015.close()


def comcheck():
	"""Check communication with the device"""

	# Just knock on the door to see if instrument is present
	idn_response = HMC8015.query_str('*IDN?')
	sleep(1)
	print('Hello, I am ' + idn_response)


def measprep():
	"""Prepare instrument for desired measurements
	There are four measurement windows with 6 cells each available
	Command is "VIEW:NUMeric:PAGE<n>:CELL<m>:FUNCtion?"

	Where <n> is number of page (1...4)
	and   <m> is number of cell (1...6-10)
	With functions

	P Active power P (Watt)
	S Apparent power S (VA)
	Q Reactive power Q (var)
	LAMBda Power factor λ (PF)
	PHI Phase difference Φ ( ° )
	FU Voltage frequency fU (V)
	FI Current frequency fI (A)
	URMS True rms voltage Urms (V)
	UAVG Voltage average (V)
	IRMS True rms current Irms (A)
	IAVG Current average (A)
	UTHD Total harmonic distortion of voltage Uthd (THD %)
	ITHD Total harmonic distortion of current Ithd (THD %)
	FPLL PLL source frequency fPLL (Hz)
	TIME Integration time
	WH Watt hour (Wh)
	WHP Positive watt hour (Wh)
	WHM Negative watt hour (Wh)
	AH Ampere hour (Ah)
	AHP Positive ampere hour (Ah)
	AHM Negative ampere hour (Ah)
	URANge Voltage range
	IRANge Current range
	EMPTy Empty cell
	"""

	HMC8015.write_str_with_opc('VIEW:NUMeric:PAGE1:CELL1:FUNCtion URMS')  # Page1 Cell1 to root mean square voltage
	HMC8015.write_str_with_opc('VIEW:NUMeric:PAGE1:CELL2:FUNCtion UAVG')  # Page1 Cell2 to average voltage
	HMC8015.write_str_with_opc('VIEW:NUMeric:PAGE1:CELL3:FUNCtion IRMS')  # Page1 Cell3 to root mean square current
	HMC8015.write_str_with_opc('VIEW:NUMeric:PAGE1:CELL4:FUNCtion IAVG')  # Page1 Cell4 to average current
	HMC8015.write_str_with_opc('VIEW:NUMeric:PAGE1:CELL5:FUNCtion P')     # Page1 Cell5 to active power
	HMC8015.write_str_with_opc('VIEW:NUMeric:PAGE1:CELL6:FUNCtion S')     # Page1 Cell6 to apparent power


def log():
	"""Define and begin logging for all 6 set measurements (on 1st screen).
	Also check the directory if the file exists after logging process is complete."""

	try:  # Delete the logfile (if already existing) and
		HMC8015.write_str_with_opc(f'DATA:DELETE "{log_file_name}",EXT')  # insert a try block to prevent throwing an
	except StatusException:  # error when the log file to be deleted is
		pass  # not present

	HMC8015.write_int_with_opc('LOG:PAGE ', pagenum)  # The defined page (pagenum) will be used for logging (is default value, just to show)
	HMC8015.write_str_with_opc('LOG:MODE DURation')  # Log mode is set to a dedicated time
	HMC8015.write_int_with_opc('LOG:DURation ', logdur)  # Set dedicated time (lodur) in seconds for logging duration
	HMC8015.write_str_with_opc('LOG:INTerval MIN')  # Change the logging interval to minimum (100ms)
	HMC8015.write_str_with_opc(f'LOG:FNAME "{log_file_name}",EXT')  # Define name (log_file_name) and location for the log file
	HMC8015.write_str_with_opc('LOG:STATe ON')  # Now start logging
	sleep(int(logdur))  # Wait for the log to be written
	file_response = HMC8015.query_str('DATA:LIST? EXT')  # Read out directory content
	print(file_response)


def fileget():
	"""Transfer the log file to the local PC"""

	HMC8015.data_chunk_size = 10000  # Define Chunk size (helps with bigger files)
	append = False
	pc_file_path = r'c:\temp\logdata.csv'
	print('Transferring the log file...')
	HMC8015.query_bin_block_to_file(f'DATA:DATA? "{log_file_name}",EXT', pc_file_path, append)  # Directly stream the file to local PC
	print(f'File saved to {pc_file_path}')
	HMC8015.write_str_with_opc(f'DATA:DELETE "{log_file_name}",EXT')  # Delete the log file after completion


# -------------------------
# Main Program begins here
# -------------------------


comprep()
comcheck()
measprep()
log()
fileget()
close()

print("Programm succesfully ended.")
