# GitHub examples repository path: Oscilloscopes/Python/RsInstrument
# Example for RTO / RTE / RTP Oscilloscopes
# Preconditions:
# - Installed RsInstrument Python module from pypi.org
# - Installed VISA e.g. R&S Visa 5.12.x or newer

from RsInstrument import *  # The RsInstrument package is hosted on pypi.org, see Readme.txt for more details
from time import time

# Make sure you have the last version of the RsInstrument
RsInstrument.assert_minimum_version('1.53.0')
rto = None
try:
	rto = RsInstrument('TCPIP::192.168.2.10::INSTR', True, False)
	rto.visa_timeout = 3000  # Timeout for VISA Read Operations
	rto.opc_timeout = 15000  # Timeout for opc-synchronised operations
	rto.instrument_status_checking = True  # Error check after each command
except Exception as ex:
	print('Error initializing the instrument session:\n' + ex.args[0])
	exit()

print(f'rto2000 IDN: {rto.idn_string}')
print(f'rto2000 Options: {",".join(rto.instrument_options)}')

rto.clear_status()
rto.reset()
rto.write_str("SYST:DISP:UPD ON")  # Display update ON - switch OFF after debugging

# -----------------------------------------------------------
# Basic Settings:
# ---------------------------- -------------------------------
rto.write_str("ACQ:POIN:AUTO RECL")  # Define Horizontal scale by number of points
rto.write_str("TIM:RANG 0.01")  # 10ms Acquisition time
rto.write_str("ACQ:POIN 20002")  # 20002 X points
rto.write_str("CHAN1:RANG 2")  # Horizontal range 2V
rto.write_str("CHAN1:POS 0")  # Offset 0
rto.write_str("CHAN1:COUP AC")  # Coupling AC 1MOhm
rto.write_str("CHAN1:STAT ON")  # Switch Channel 1 ON

# -----------------------------------------------------------
# Trigger Settings:
# -----------------------------------------------------------
rto.write_str("TRIG1:MODE AUTO")  # Trigger Auto mode in case of no signal is applied
rto.write_str("TRIG1:SOUR CHAN1")  # Trigger source CH1
rto.write_str("TRIG1:TYPE EDGE;:TRIG1:EDGE:SLOP POS")  # Trigger type Edge Positive
rto.write_str("TRIG1:LEV1 0.04")  # Trigger level 40mV
rto.query_opc()  # Using *OPC? query waits until all the instrument settings are finished

# -----------------------------------------------------------
# SyncPoint 'SettingsApplied' - all the settings were applied
# -----------------------------------------------------------
# Arming the rto for single acquisition
# -----------------------------------------------------------
rto.visa_timeout = 2000  # Acquisition timeout - set it higher than the acquisition time
rto.write_str("SING")
# -----------------------------------------------------------
# DUT_Generate_Signal() - in our case we use Probe compensation signal
# where the trigger event (positive edge) is reoccurring
# -----------------------------------------------------------
rto.query_opc()  # Using *OPC? query waits until the instrument finished the Acquisition
# -----------------------------------------------------------
# SyncPoint 'AcquisitionFinished' - the results are ready
# -----------------------------------------------------------
# Fetching the waveform in ASCII and BINary format
# -----------------------------------------------------------
t = time()
trace = rto.query_bin_or_ascii_float_list('FORM ASC;:CHAN1:DATA?')  # Query ascii array of floats
print(f'Instrument returned {len(trace)} points in the ascii trace, query duration {time() - t:.3f} secs')
t = time()
rto.bin_float_numbers_format = BinFloatFormat.Single_4bytes  # This tells the driver in which format to expect the binary float data
trace = rto.query_bin_or_ascii_float_list('FORM REAL,32;:CHAN1:DATA?')  # Query binary array of floats - the query function is the same as for the ASCII format
print(f'Instrument returned {len(trace)} points in the binary trace, query duration {time() - t:.3f} secs')

# -----------------------------------------------------------
# Making an instrument screenshot and transferring the file to the PC
# -----------------------------------------------------------
rto.write_str('HCOP:DEV:LANG PNG')  # Set the screenshot format
rto.write_str(r"MMEM:NAME 'c:\temp\Dev_Screenshot.png'")  # Set the screenshot path
rto.write_str("HCOP:IMM")  # Make the screenshot now
rto.query_opc()  # Wait for the screenshot to be saved
rto.read_file_from_instrument_to_pc(r'c:\temp\Dev_Screenshot.png', r'c:\Temp\PC_Screenshot.png')  # Query the instrument file to the PC
print(r"Screenshot file saved to PC 'c:\Temp\PC_Screenshot.png'")

# Close the session
rto.close()
