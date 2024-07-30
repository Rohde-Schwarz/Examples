"""
# GitHub examples repository path: : Powersensors/Python/RsInstrument

This Python example shows how to perform pulse analysis using an adequate power sensor.
The script will perform a dedicated number of measurements in a row to display some pulse
relevant measurement parameters.
The script is prepared for a test signal with the following parameters:
f = 1 GHz, -10 dBm, Pulse Modulation (PRI = 1 ms, Pulse Width = 200 µs).
After changing the variables, any other signal setup can be chosen.

Preconditions:
- Installed RsInstrument Python module from pypi.org
- Installed VISA e.g. R&S Visa 5.12.x or newer

Tested with:
- NRP18P, FW V 01.30.24040901
- NRP-Z85 FW V 01.37

- Python 3.12
- RsInstrument 1.82.1

Author: R&S Product Management AE 1GP3 / PJ
Updated on 29.07.2024
Version: v1.0

Technical support -> https://www.rohde-schwarz.com/support

Before running, please always check your setup!
This example does not claim to be complete. All information have been
compiled with care. However, errors can’t be ruled out.

"""

# --> Import necessary packets
from RsInstrument import *
from time import sleep
from math import log10
from math import isnan

# Define variables
# resource = 'RSNRP::0x0083::102966::INSTR'  # VISA resource string for NRP-Z8x with legacy interface
resource = 'USB::0x0AAD::0x0143::100104::INSTR'  # VISA resource string for NRPxxP/S USB sensor

n_o_loops = 10  # Number of measurements to take
freq = 1e+09  # Signal frequency in Hz
pri = 2e-03  # PRI = Pulse Repetition Interval (period) in s
no_pri = 5  # Number PRIs to read in one trace
points = 500  # Nuber of trace points to take
trg_lev = 8e-05  # Trigger level in W
offset = 2e-04  # Offset time to compensate trigger reaction / offset time in s

# Define the device handle
nrp = RsInstrument(resource, False, True, options="SelectVisa='rs'")


# Define all the subroutines

def com_prep():
    """Preparation of the communication (termination, etc...)"""
    print(f'\nVISA Manufacturer: {nrp.visa_manufacturer}\n')  # Confirm VISA package / manufacturer
    nrp.visa_timeout = 3000  # Timeout for VISA Read Operations
    nrp.opc_timeout = 3000  # Timeout for opc-synchronised operations
    nrp.instrument_status_checking = True  # Error check after each command, can be True or False
    nrp.clear_status()
    nrp.logger.log_to_console = False  # Route SCPI logging feature to console on (True) or off (False)
    nrp.logger.mode = LoggingMode.Off  # Switch On or Off SCPI logging


def com_check():
    """Test the device connection, request ID as well as installed options"""
    print('Hello, I am ' + nrp.query('*IDN?'), end=" ")


def prepare():
    """Set all the parameters before performing measurement(s)"""
    nrp.write(f'SENSe:FREQ {freq}')  # Set measurement frequency
    nrp.write('SENS:FUNC "XTIM:POW"')  # Switch to trace measurement
    nrp.write('INIT:CONT OFF')  # Switch off Continuous Mode
    nrp.write(f'SENS:TRAC:POIN {points}')  # Set number of measurement points to be recorded for each trace
    nrp.write(f'SENS:TRAC:TIME {pri*no_pri}')  # Length of the trace record
    nrp.write(f'SENS:TRAC:OFFS:TIME {offset}')  # Offset time to compensate trigger reaction / offset time
    nrp.write('TRIG:SOUR INT')  # Trigger source to internal (starting with the measurement signal)
    nrp.query_opc()  # Check for command completion in between
    nrp.write('TRIG:SLOP POS')  # Trigger slope is positive now
    nrp.write('TRIG:COUN 1')  # Start capturing after only one single trigger event
    nrp.write(f'TRIG:LEV {trg_lev}')  # Set the trigger level to desired value (W)
    nrp.write('SENS:TRAC:AVER:COUN 1')
    nrp.write('SENS:TRAC:MEAS:STAT ON')  # Enables measurement statistics for trace measurements.
    nrp.write(f'SENSe:TRAC:MEAS:TIME {pri*no_pri}')
    nrp.query_opc()  # Check for command completion at the end


def measure():
    """ Perform Trace / Pulse measurements"""
    x = 0
    while x < n_o_loops:
        nrp.write('INITiate:IMMediate')  # Start single measurement
        sleep(1)  # Wait for one second, so that the signal can be triggered and captured completely
        print(f'\nMeasurement N°{x+1}')
        try:
            test = (nrp.query_float('SENS:TRAC:MEAS:POW:AVG?'))  # Check for a valid signal before measuring
        except ValueError:  # NRP-Z sensors will throw a ValueError as long as there is no valid signal available
            print('Cannot measure. Either timing information is wrong, signal level is too low, trigger level is too ')
            print('high or signal is not present. Please check your setup and try again.')
            exit()
        if isnan(test):  # NRP-xxP sensors return a "nan-float" as long as there is no valid signal available
            print('Cannot measure. Either timing information is wrong, signal level is too low, trigger level is too ')
            print('high or signal is not present. Please check your setup and try again.')
            exit()
        #  Now perform all the measurements and display the formatted data
        print(f'Duty cycle is {nrp.query_float('SENS:TRAC:MEAS:PULS:DCYC?'):.3f} %')

        print(f'Pulse duration is {nrp.query_float('SENS:TRAC:MEAS:PULS:DUR?')*1e3:.3f} ms')

        print(f'Pulse Period (PRI) is {nrp.query_float('SENS:TRAC:MEAS:PULS:PER?')*1e3:.3f} ms')

        print(f'Positive Transient Duration (rise time) is {nrp.query_float('SENS:TRAC:MEAS:TRAN:POS:DUR?')
                                                            * 1e6:.3f} µs')

        print(f'Positive Transient Occurrence (start time) is {nrp.query_float('SENS:TRAC:MEAS:TRAN:POS:OCC?')
                                                               * 1e6:.3f} µs')

        print(f'Positive Transient Overshoot is {nrp.query_float('SENS:TRAC:MEAS:TRAN:POS:OVER?'):.3f} %')

        print(f'Negative Transient Duration (fall time) is {nrp.query_float('SENS:TRAC:MEAS:TRAN:NEG:DUR?')
                                                            * 1e6:.3f} µs')

        print(f'Negative Transient Occurrence (end time) is {nrp.query_float('SENS:TRAC:MEAS:TRAN:NEG:OCC?')
                                                             * 1e6:.3f} µs')

        print(f'Negative Transient Overshoot is {nrp.query_float('SENS:TRAC:MEAS:TRAN:NEG:OVER?'):.3f} %')

        av_pow = nrp.query_float('SENS:TRAC:MEAS:POW:AVG?')
        print(f'Average Power over period is {av_pow * 1e3:.3f} mW / {10 * log10(av_pow * 1e3):.3f} dBm')

        min_pow = nrp.query_float('SENS:TRAC:MEAS:POW:MIN?')
        print(f'Minimum Power captured is {min_pow * 1e3:.3f} mW / {10 * log10(abs(min_pow) * 1e3):.3f} dBm')

        max_pow = nrp.query_float('SENS:TRAC:MEAS:POW:MAX?')
        print(f'Maximal Power captured is {max_pow * 1e3:.3f} mW / {10 * log10(max_pow * 1e3):.3f} dBm')

        ptop_pow = nrp.query_float('SENS:TRAC:MEAS:POW:PULS:TOP?')
        print(f'Pulse Top Power is {ptop_pow * 1e3:.3f} mW / {10 * log10(ptop_pow * 1e3):.3f} dBm')

        p_base_pow = nrp.query_float('SENS:TRAC:MEAS:POW:PULS:BASE?')
        print(f'Pulse Base Power is {p_base_pow * 1e3:.3f} mW / {10 * log10(abs(p_base_pow) * 1e3):.3f} dBm')

        print(f'The Time Resolution of the measurements is {nrp.query_float('SENS:TRAC:MEAS:TRAN:SPER?')*1e6:.3f} µs')
        print('\n')
        x += 1


def close():
    """Close the VISA session"""
    nrp.close()


#  Main program begins here
com_prep()
com_check()
prepare()
measure()
close()

print("Program successfully ended.")
