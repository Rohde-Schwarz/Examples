# Example for FSW / FSV / FSVA / FPS Spectrum Analyzers
# Preconditions:
# - Installed RsInstrument Python module Version 1.9.0 or newer from pypi.org
# - Installed VISA e.g. R&S Visa 5.12.x or newer

from RsInstrument import *  # The RsInstrument package is hosted on pypi.org, see Readme.txt for more details
from time import time

specan = None
RsInstrument.assert_minimum_version('1.10.0')
try:
	# Adjust the VISA Resource string to fit your instrument
	specan = RsInstrument('TCPIP::localhost::INSTR', True, False)
	specan.visa_timeout = 3000  # Timeout for VISA Read Operations
	specan.opc_timeout = 3000  # Timeout for opc-synchronised operations
	specan.instrument_status_checking = True  # Error check after each command
except Exception as ex:
	print('Error initializing the instrument session:\n' + ex.args[0])
	exit()

print(f'Driver Version: {specan.driver_version}')
print(f'SpecAn IDN: {specan.idn_string}')
print(f'SpecAn Options: {",".join(specan.instrument_options)}')

specan.clear_status()
specan.reset()
specan.write_str('INIT:CONT OFF')  # Switch OFF the continuous sweep
specan.write_str('SYST:DISP:UPD ON')  # Display update ON - switch OFF after debugging
# -----------------------------------------------------------
# Basic Settings:
# -----------------------------------------------------------
specan.write_str('DISP:WIND:TRAC:Y:RLEV 10.0')  # Setting the Reference Level
specan.write_str('FREQ:CENT 3.0 GHz')  # Setting the center frequency
specan.write_str('FREQ:SPAN 200 MHz')  # Setting the span
specan.write_str('BAND 100 kHz')  # Setting the RBW
specan.write_str('BAND:VID 300kHz')  # Setting the VBW
specan.write_str('SWE:POIN 10001')  # Setting the sweep points
specan.query_opc()  # Using *OPC? query waits until all the instrument settings are finished
# -----------------------------------------------------------
# SyncPoint 'SettingsApplied' - all the settings were applied
# -----------------------------------------------------------
specan.VisaTimeout = 2000  # Sweep timeout - set it higher than the instrument acquisition time
specan.write_str_with_opc('INIT')  # Start the sweep and wait for it to finish
# -----------------------------------------------------------
# SyncPoint 'AcquisitionFinished' - the results are ready
# -----------------------------------------------------------
# Fetching the trace
# The functions are universal for binary or ascii data format
# -----------------------------------------------------------
t = time()
trace = specan.query_bin_or_ascii_float_list('FORM ASC;:TRAC? TRACE1')  # Query ascii array of floats
print(f'Instrument returned {len(trace)} points in the ascii trace, query duration {time() - t:.3f} secs')
t = time()
specan.bin_float_numbers_format = BinFloatFormat.Single_4bytes  # This tells the driver in which format to expect the binary float data
trace = specan.query_bin_or_ascii_float_list('FORM REAL,32;:TRAC? TRACE1')  # Query binary array of floats - the query function is the same as for the ASCII format
print(f'Instrument returned {len(trace)} points in the binary trace, query duration {time() - t:.3f} secs')
# -----------------------------------------------------------
# Setting the marker to max and querying the X and Y
# -----------------------------------------------------------
specan.write_str_with_opc('CALC1:MARK1:MAX')  # Set the marker to the maximum point of the entire trace, wait for it to be set
markerX = specan.query_float('CALC1:MARK1:X?')
markerY = specan.query_float('CALC1:MARK1:Y?')
print(f'Marker Frequency {markerX:.2f} Hz, Level {markerY:.3f} dBm')
# -----------------------------------------------------------
# Making an instrument screenshot and transferring the file to the PC
# -----------------------------------------------------------
specan.write_str("HCOP:DEV:LANG PNG")
specan.write_str(r"MMEM:NAME 'c:\temp\Dev_Screenshot.png'")
specan.write_str("HCOP:IMM")  # Make the screenshot now
specan.query_opc()  # Wait for the screenshot to be saved
specan.read_file_from_instrument_to_pc(r"c:\temp\Dev_Screenshot.png", r"c:\Temp\PC_Screenshot.png")  # Transfer the instrument file to the PC
print(r"Instrument screenshot file saved to PC 'c:\Temp\PC_Screenshot.png'")

# Close the session
specan.close()
