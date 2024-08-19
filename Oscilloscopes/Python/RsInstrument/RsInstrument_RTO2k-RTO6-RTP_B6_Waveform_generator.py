# GitHub examples repository path: Oscilloscopes/Python/RsInstrument

"""

Created on 2022/07

Author: Jahns_P
Version Number: 1
Date of last change: 2022/07/22
Requires: R&S RTO2000, RTO6 or RTP with FW 1.600 or newer and B6 option (Waveform generator)
- B6 GEN1 must be connected to CH1 to display correct results
- Installed RsInstrument Python module (see the attached RsInstrument_PythonModule folder Readme.txt)
- Installed VISA e.g. R&S Visa 5.12.x or newer

Description: Example about how to use the Waveform Generator (B6) with sine and ARB wave

General Information:
This example does not claim to be complete. All information has been
compiled with care. However, errors can not be ruled out.
"""

import time

from RsInstrument import *

PcFilePath = r"c:\tempdata\waveform.csv"
InstFilePath = r"c:\Users\Public\Documents\Rohde-Schwarz\Rtx\RefWaveforms\testform.csv"

# ================================
# Prepare instrument communication
# ================================

resource = 'TCPIP0::10.205.0.103::inst0::INSTR'  # Assign Instrument VISA resource string

RsInstrument.assert_minimum_version("1.50")  # Check for RsInstrument version and stop if version number is too low
rto = RsInstrument(resource, reset=True, id_query=False,
                   options="SelectVisa='rs' , LoggingMode = Off, LoggingToConsole = False")

rto.instrument_status_checking = False  # Error check after each command MUST BE OFF for this instrument
rto.visa_timeout = 5000  # Timeout for VISA Read Operations
rto.opc_timeout = 5000  # Timeout for opc-synchronised operations
rto.clear_status()  # Clear status register


def devcheck():
    """Request Identification string and options"""
    print(rto.query_str('*IDN?'))  # Request and print IDN string
    rto.write('SYSTem:DISPlay:UPDate ON')  # Set display on while instrument is remote controlled
    options = rto.instrument_options  # Request instrument options
    nopt = len(options)
    print('This instrument is equipped with the following ', nopt, 'different options:')
    x = 0
    while x < nopt:
        print(options[x], ", ", end="")
        x += 1
    print('\n')


def funcprep():
    """Prepare function generator for first measurement"""
    rto.write_str('WGENerator1:SOURce FUNCgen')  # Activate function generator
    # Possible values: FUNCgen | MODulation | SWEep | ARBGenerator
    rto.write_str('WGENerator1:FUNCtion:SELect SINusoid')  # Wave form is sinusoidal
    # Possible values: SINusoid | SQUare | RAMP | DC | PULSe | SINC | CARDiac | GAUSs | LORNtz | EXPRise | EXPFall
    rto.write_str('WGENerator1:FREQuency 10MHZ')  # Set frequency (range = 1E-3 to 100E+6)
    rto.write_str('WGENerator1:VOLTage:VPP 200 MV')  # Set output level to 200 mV pp (range = 0.01 to 12 V)
    rto.write_str('WGENerator1:VOLTage:DCLevel 0V')  # Additional DC level is 0V (range: -5.999 to 5.995 V)
    rto.write_str('WGENerator1:OUTPut HIZ')  # Set output impedance to HiZ (possible values: FIFTy | HIZ)
    rto.write_str('WGENerator1:ENABle ON')  # Enable generator output
    rto.query_opc()


def arbprep():
    """Generate and write a waveform file to the scope, load and start it
       See also in Chapter 15.1.5 ("Arbitrary") of the manual """

    # One example to provide a square waveform, but rather use more steps to avoid voltage spikes in this case.
    '''
    file = open(r"c:\tempdata\waveform.csv", 'w')  # Open local file to be written
    file.write('Rate = 1000000  // Sample rate for the ARB file\n')
    file.write('0.00E-3, 0.00  // @ 0 ms, 0 V\n')
    file.write('0.01E-3, 0.01  // @ 10 µs, 0.01 V\n')  # Smoothen the flanks to avoid over- and undershooting
    file.write('0.02E-3, 0.49  // @ 20 µs, 0.49 V\n')
    file.write('0.03E-3, 0.50  // @ 30 µs, 0.5 V\n')  # Main voltage for HI level
    file.write('9.98E-3, 0.50  // @ 9.98 ms, 0.5 V\n')
    file.write('9.99E-3, 0.49  // @ 9.99 ms, 0.49 V\n')  # Smoothen the flanks to avoid over- and undershooting
    file.write('10.00E-3, 0.01  // @ 10 ms, 0.01 V\n')
    file.write('10.01E-3, 0.00  // @ 10.01 ms, 0 V\n')  # Main voltage for LO level
    file.write('19.99E-3, 0.00  // @ 19.99 ms, 0 V\n')
    file.close()
    '''

    # Another way to generate an ARB waveform (square signal) only using sample rate and voltage values

    nofsamples = 96  # Number of samples for one half ARB curve (minus number of smoothing points)

    file = open(r"c:\tempdata\waveform.csv", 'w')  # Open local file to be written
    file.write('Rate = 100000  // Sample rate for the ARB file\n')
    file.write('0.0\n')  # Write voltage steps into the WF file
    file.write('0.01\n')  # Smoothen the flanks to avoid over- and undershooting
    file.write('0.2\n')  # before writing the main points for the first part of the square wave
    file.write('0.4\n')
    file.write('0.49\n')
    x = 0
    while x < nofsamples:  # Complete first part of the waveform in a loop with the same values
        file.write('0.5\n')
        x += 1
    file.write('0.49\n')  # Smoothen the flanks to avoid over- and undershooting
    file.write('0.4\n')  # after writing the main points for the first part of the square wave
    file.write('0.2\n')
    file.write('0.01\n')
    x = 0
    while x < nofsamples-1:  # Complete second part of the waveform in a loop with the same values
        file.write('0.0\n')
        x += 1
    file.close()

    rto.send_file_from_pc_to_instrument(PcFilePath, InstFilePath)
    rto.query_opc()
    rto.write_str('WGENerator1:SOURce ARBGenerator')  # Activate function generator
    rto.write_str(f'WGENerator1:ARBGen:NAME {InstFilePath}')  # Define ARB file to be opened
    rto.write_str('WGENerator1:ARBGen:OPEN')  # Open and apply the specific ARB file
    rto.write_str('WGENerator1:ARBGen:SRATe 5000000')  # Define a sample rate separate from the ARB file
    rto.write_str('WGENerator1:ARBGen:RUNMode CONTinuous')  # Switch generator to endless repeat loop
    rto.query_opc()  # Check for command completion
    print('Number of Samples in waveform is ' + rto.query('WGENerator1:ARBGen:SAMPles?'))


def measprep():
    """Prepare the scope for measurement"""
    rto.write_str('ACQuire:COUNt 20')  # Acquire 20 waveforms to calculate average waveform
    rto.write_str("TRIGger1:SOURce CHAN1")  # Define trigger source
    rto.write_str('TRIGger1:MODe NORMal')  # Trigger mode is normal
    rto.write_str('SINGle')  # Single trigger operations
    rto.write_str('AUToscale')  # Perform auto scaling
    rto.query_opc()  # Check for command completion


def measure():
    """Perform measurement and display waveform on PC"""
    rto.write_str('SINGle')  # Initiate single trigger measurement
    trace = rto.query_bin_or_ascii_float_list('FORM ASC;:CHAN1:DATA?')  # Query ascii array of floats
    print(f'The scope returned {len(trace)} measurement points.')  # Analyze the data


def close():
    rto.close()


def main():
    devcheck()
    funcprep()
    measprep()
    measure()
    time.sleep(10)  # Some pause between the two generator modes
    arbprep()
    measprep()
    measure()
    close()


main()
print("I'm done")
