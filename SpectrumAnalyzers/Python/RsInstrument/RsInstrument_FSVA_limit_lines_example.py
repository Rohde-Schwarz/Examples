# GitHub examples repository path: SpectrumAnalyzers/Python/RsInstrument
# Example for FSW / FSV / FSVA / FPS Spectrum Analyzers
# Preconditions:
# - Installed RsInstrument Python module from pypi.org
# - Installed VISA e.g. R&S Visa 5.12.x or newer

from RsInstrument import *  # The RsInstrument package is hosted on pypi.org, see Readme.txt for more details

io = None
RsInstrument.assert_minimum_version('1.82.1')
try:
	# Adjust the VISA Resource string to fit your instrument
	io = RsInstrument('TCPIP::localhost::INSTR', True, False)
	io.visa_timeout = 3000  # Timeout for VISA Read Operations
	io.opc_timeout = 3000  # Timeout for opc-synchronised operations
	io.instrument_status_checking = True  # Error check after each command
except Exception as ex:
	print('Error initializing the instrument session:\n' + ex.args[0])
	exit()

# --------------Preparing the instrument ---------------------
io.query_with_opc('*RST;*OPC?')
# Resets the instrument
io.write('INIT:CONT OFF')
# Selects single sweep mode.
io.write('SYStem:DISPlay:UPDate ON')

# ------------- Configuring the limit lines ---------------------
io.write("CALC:LIM1:NAME 'FM1'")
# Names limit line 1 'FM1'.

io.write('CALC:LIM1:CONT:MODE ABS')
# Selects absolute scaling for the horizontal axis.
io.write('CALC:LIM1:CONT 1 MHz,50MHz,100 MHz,150MHz,200MHz')
# Defines 5 horizontal definition points for limit line 1.
io.write('CALC:LIM1:UPP:MODE ABS')
# Selects an absolute vertical scale for limit line 1.
io.write('CALC:LIM1:UNIT DBM')
# Selects the unit dBm for limit line 1.
io.write('CALC:LIM1:UPP -10,-5,0,-5,-10')
# Defines 5 definition points for limit line 1.

io.write('CALC:LIM1:UPP:MARG 5dB')
# Defines an area of 5 dB around limit line 1 where limit check violations
# are still tolerated.

io.write('CALC:LIM1:UPP:SHIF -10DB')
# Shifts the limit line 1 by -10 dB.
io.write('CALC:LIM1:UPP:OFFS -3dB')
# Defines an additional -3 dB offset for limit line 1.

io.write("CALC:LIM3:NAME 'FM3'")
# Names limit line 3 'FM3'.

io.write('CALC:LIM3:LOW:MODE REL')
# Selects a relative vertical scale for limit line 3.
io.write('CALC:LIM3:UNIT DB')

io.write('CALC:LIM3:CONT 1 MHz,50MHz,100 MHz,150MHz,200MHz')
# Defines 5 horizontal definition points for limit line 3.
io.write('CALC:LIM3:LOW -90,-60,-40,-60,-90')
# Defines 5 definition points relative to the reference level for limit line 3.

io.write('CALC:LIM3:LOW:SHIF 2')
# Shifts the limit line 3 by 2dB.
io.write('CALC:LIM3:LOW:OFFS 3')
# Defines an additional 3 dB offset for limit line 3.

io.write('CALC:LIM3:LOW:THR -200DBM')
# Defines a power threshold of -200dBm that must be exceeded for limit to be checked

io.write('CALC:LIM3:LOW:MARG 5dB')
# Defines an area of 5dB around limit line 3 where limit check violations
# are still tolerated.

# --------------Configuring the measurement -------------
io.write('FREQ:CENT 100MHz')
# Defines the center frequency
io.write('FREQ:SPAN 200MHz')
# Sets the span to 100 MHz on either side of the center frequency.
io.write('SENS:SWE:COUN 10')
# Defines 10 sweeps to be performed in each measurement.
io.write('DISP:TRAC1:Y:RLEV 0dBm')
# Sets the reference level to 0 dBm.
io.write('TRIG:SOUR IFP')
io.write('TRIG:LEV:IFP -10dBm')
# Defines triggering when the second intermediate frequency rises to a level
# of -10 dBm.

# --------------Configuring the Trace--------------------------
io.write('DISP:TRAC2 ON')
io.write('DISP:TRAC2:MODE AVER')
io.write('DISP:TRAC3 ON')
io.write('DISP:TRAC3:MODE MAXH')
# Configures 3 traces: 1 (default): clear/write; 2: average; 3: max hold

# ------------- Configuring the limit check -------------------
io.write("CALC:LIM1:NAME 'FM1'")
io.write('CALC:LIM1:UPP:STAT ON')
# Activates upper limit FM1 as line 1.
io.write("CALC:LIM3:NAME 'FM3'")
io.write('CALC:LIM3:LOW:STAT ON')
# Activates lower limit line FM3 as line 3.
resp = io.query('CALC:LIM:ACT?')
# Queries the names of all active limit lines
# Result: 'FM1,FM3'
io.write('CALC:LIM1:TRAC3:CHEC ON')
# Activates the upper limit to be checked against trace3 (maxhold trace)
io.write('CALC:LIM3:TRAC2:CHEC ON')
# Activates the upper limit to be checked against trace2 (average trace)
io.write('CALC:LIM:CLE')
# Clears the previous limit check results

# ------------- Performing the measurement---------------------
io.write('INIT;*WAI')
# Initiates a new measurement and waits until the last sweep has finished.

# -------------- Retrieving limit check results----------------------------

lim1_fail = io.query('CALC:LIM1:FAIL?')  # Queries the result of the upper limit line check
print('Limit 1 fail: ' + lim1_fail)
lim2_fail = io.query('CALC:LIM3:FAIL?')  # Queries the result of the lower limit line check
print('Limit 2 fail: ' + lim2_fail)
