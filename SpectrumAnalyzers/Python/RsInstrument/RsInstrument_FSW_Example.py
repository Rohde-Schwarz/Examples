# GitHub examples repository path: SpectrumAnalyzers/Python/RsInstrument
# Example for FSW / FSV / FSVA / FPS Spectrum Analyzers
# Preconditions:
# - Installed RsInstrument Python module from pypi.org
# - Installed VISA e.g. R&S Visa 5.12.x or newer

from RsInstrument import *  # The RsInstrument package is hosted on pypi.org, see Readme.txt for more details
from time import time

fsw = None
RsInstrument.assert_minimum_version('1.53.0')
try:
	# Adjust the VISA Resource string to fit your instrument
	fsw = RsInstrument('TCPIP::localhost::INSTR', True, False)
	fsw.visa_timeout = 3000  # Timeout for VISA Read Operations
	fsw.opc_timeout = 3000  # Timeout for opc-synchronised operations
	fsw.instrument_status_checking = True  # Error check after each command
except Exception as ex:
	print('Error initializing the instrument session:\n' + ex.args[0])
	exit()

print(f'Driver Version: {fsw.driver_version}')
print(f'SpecAn IDN: {fsw.idn_string}')
print(f'SpecAn Options: {",".join(fsw.instrument_options)}')

fsw.clear_status()
fsw.reset()
fsw.write_str('INIT:CONT ON')  # Switch OFF the continuous sweep
fsw.write_str('SYST:DISPlay:')  # Display update ON - switch OFF after debugging
# -----------------------------------------------------------
# Basic Settings:
# -----------------------------------------------------------
fsw.write_str('DISPlay:WINDow:TRACe:Y:SCALe:RLEVel 10DBM')  # Setting the Reference Level
fsw.write_str('FREQ:CENT 3.0 GHz')  # Setting the center frequency
fsw.write_str('FREQ:SPAN 200 MHz')  # Setting the span
fsw.write_str('BAND 100 kHz')  # Setting the RBW
fsw.write_str('BAND:VID 300kHz')  # Setting the VBW
fsw.write_str('SWE:POIN 10001')  # Setting the sweep points
fsw.query_opc()  # Using *OPC? query waits until all the instrument settings are finished
# -----------------------------------------------------------
# SyncPoint 'SettingsApplied' - all the settings were applied
# -----------------------------------------------------------
fsw.VisaTimeout = 2000  # Sweep timeout - set it higher than the instrument acquisition time
fsw.write_str_with_opc('INIT')  # Start the sweep and wait for it to finish
# -----------------------------------------------------------
# SyncPoint 'AcquisitionFinished' - the results are ready
# -----------------------------------------------------------
# Fetching the trace
# The functions are universal for binary or ascii data format
# -----------------------------------------------------------
t = time()
trace = fsw.query_bin_or_ascii_float_list('FORM ASC;:TRAC? TRACE1')  # Query ascii array of floats
print(f'Instrument returned {len(trace)} points in the ascii trace, query duration {time() - t:.3f} secs')
t = time()
fsw.bin_float_numbers_format = BinFloatFormat.Single_4bytes  # This tells the driver in which format to expect the binary float data
trace = fsw.query_bin_or_ascii_float_list('FORM REAL,32;:TRAC? TRACE1')  # Query binary array of floats - the query function is the same as for the ASCII format
print(f'Instrument returned {len(trace)} points in the binary trace, query duration {time() - t:.3f} secs')
# -----------------------------------------------------------
# Setting the marker to max and querying the X and Y
# -----------------------------------------------------------
fsw.write_str_with_opc('CALC1:MARK1:MAX')  # Set the marker to the maximum point of the entire trace, wait for it to be set
markerX = fsw.query_float('CALC1:MARK1:X?')
markerY = fsw.query_float('CALC1:MARK1:Y?')
print(f'Marker Frequency {markerX:.2f} Hz, Level {markerY:.3f} dBm')
# -----------------------------------------------------------
# Making an instrument screenshot and transferring the file to the PC
# -----------------------------------------------------------
fsw.write_str("HCOP:DEV:LANG PNG")
fsw.write_str(r"MMEM:NAME 'c:\temp\Dev_Screenshot.png'")
fsw.write_str("HCOP:IMM")  # Make the screenshot now
fsw.query_opc()  # Wait for the screenshot to be saved
fsw.read_file_from_instrument_to_pc(r"c:\temp\Dev_Screenshot.png", r"c:\Temp\PC_Screenshot.png")  # Transfer the instrument file to the PC
print(r"Instrument screenshot file saved to PC 'c:\Temp\PC_Screenshot.png'")

# Close the session
fsw.close()
