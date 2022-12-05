# GitHub examples repository path: SpectrumAnalyzers/Python/RsInstrument
# Example for FSW / FSV / FSVA / FPS Spectrum Analyzers
# Example for FSW showing binary IQ data read from the instrument and displayed as power spectrum
# Preconditions:
# - Installed RsInstrument Python module from pypi.org
# - Installed VISA e.g. R&S Visa 5.12.x or newer

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from RsInstrument import *  # The RsInstrument package is hosted on pypi.org, see Readme.txt for more details

# Variables
IP = '10.102.72.182'  # Analyzer IP address
fs = 100e6 			  # Sample rate (Hz)
ct = 1e-3			  # Capture time (sec)
freq = 3.9e9		  # Center frequency (Hz)
RefLev = -10		  # Reference level (dBm)

#############################################################################

# Open connection
fsw = None
RsInstrument.assert_minimum_version('1.53.0')
try:
	# Adjust the VISA Resource string to fit your instrument
	fsw = RsInstrument('TCPIP::' + IP + '::hislip0', True, False)
	fsw.visa_timeout = 10000  # Timeout for VISA Read Operations
	fsw.opc_timeout = 10000  # Timeout for opc-synchronised operations
	fsw.instrument_status_checking = True  # Error check after each command
except Exception as ex:
	print('Error initializing the instrument session:\n' + ex.args[0])
	exit()

print(f'Driver Version: {fsw.driver_version}')
print(f'SpecAn IDN: {fsw.idn_string}')

fsw.clear_status()
fsw.reset()

################################################################################

# Basic Settings:
fsw.write_str('DISPlay:WINDow:TRACe:Y:SCALe:RLEVel ' + str(RefLev))
fsw.write_str('FREQ:CENT ' + str(freq))

# Configure IQ Analyzer
fsw.write_with_opc('INST:CRE:NEW IQ, \'IQ Analyzer\'')
fsw.write_str(':INIT:CONT OFF')
fsw.write_str(':TRAC:IQ:SRAT ' + str(fs))
fsw.write_str(':SENS:SWE:TIME ' + str(ct))
fsw.query_str_with_opc(':LAY:ADD:WIND? \'1\',BEL,FREQ')
fsw.query_opc()

# Start measurement
fsw.write_with_opc('INIT:IMM')

# Get IQ data in binary format
fsw.write_str('FORM REAL,32')
fsw.write_with_opc('TRAC:IQ:DATA:FORM IQP')
tmp = np.array(fsw.query_bin_or_ascii_float_list('TRAC:IQ:DATA:MEM?'))

# Close connection
fsw.go_to_local()
fsw.close()

########################################################################

# Create complex array of IQ data
iq = tmp[0::2] + 1j * tmp[1::2]

# FFT
N = len(iq)

# Window function
win = signal.windows.flattop(N)
# Window normalization
U = np.square(np.sum(win))

# Window the data
iq_win = iq * win

# FFT size
NFFT = 2**(N - 1).bit_length()

# FFT
IQ = np.fft.fft(iq_win, NFFT)
IQ = np.fft.fftshift(IQ)

# Move the Nyquist point to the right-hand side (pos freq) to be
# consistent with plot when looking at the positive half only.
IQ = np.concatenate((IQ[1:], IQ[0]), axis=None)

# Frequency axis
df = fs/NFFT
f = np.arange(1, NFFT+1) * df - fs/2
f = f + freq

# Power spectrum
Pxx = np.real(IQ*np.conjugate(IQ))/U

# Convert to dBm (50 Ohm load assumed)
Pxx = 10*np.log10(Pxx/50 * 1000)

# Plot
plt.plot(f, Pxx)
plt.grid()
plt.xlabel('Frequency (Hz)')
plt.ylabel('PSD (dBm)')
plt.show()
