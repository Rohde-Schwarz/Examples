"""
# GitHub examples repository path: not known yet

This Python example shows how to get the average, peak and random (sample) value from an NRQ6 trace measurement.
Please find some important information about how to deal with the sample rate in the comment lines at the measurement
section.

Preconditions:
- Installed RsInstrument Python module from pypi.org
- Installed VISA e.g. R&S Visa 5.12.x or newer

Tested with:
- NRQ6 FW 03.30.24121801

Author: R&S Product Management AE 1GP3 / PJ
Updated on 28.02.2025
Version: v1.1

Technical support -> https://www.rohde-schwarz.com/support

Before running, please always check your setup!
This example does not claim to be complete. All information have been
compiled with care. However, errors can’t be ruled out.

"""

from RsInstrument import *

# Define variables
resource = 'TCPIP::nrq6-102106.local::hislip0'  # VISA resource string for the device
samples = 1000  # Number of samples for one take

# Make sure you have the latest version of the RsInstrument
RsInstrument.assert_minimum_version('1.90.0')

# Define the device handle
try:
    nrq = RsInstrument(resource, reset=False, id_query=False, options="SelectVisa='rs'")
    nrq.visa_timeout = 3000  # Timeout for VISA Read Operations
    nrq.instrument_status_checking = True  # Error check after each command
except ResourceError as ex:
    print('Error initializing the instrument session:\n' + ex.args[0])
    exit()


def com_prep():
    """Initialize the sensor and preparation of the communication (termination, etc...)"""
    nrq.write_with_opc('*RST;*CLS')
    print(f'VISA Manufacturer: {nrq.visa_manufacturer}')  # Confirm VISA package to be chosen
    nrq.visa_timeout = 3000  # Timeout for VISA Read Operations
    nrq.opc_timeout = 3000  # Timeout for opc-synchronised operations
    nrq.instrument_status_checking = True  # Error check after each command, can be True or False
    nrq.clear_status()  # Clear status register


def close():
    """Close the VISA session"""
    nrq.close()


def com_check():
    """Check communication with the device"""
    # Just knock on the door to see if instrument is present
    print('Hello, I am ' + nrq.idn_string)
    if not nrq.full_instrument_model_name.endswith('Q6'):
        raise ValueError(f'Instrument "{nrq.full_instrument_model_name}" is not an NRQ6. This example only works'
                         f'with the NRQ6 Frequency Selective Power Sensor.')


def meas_setup():
    """Prepare the sensor for the measurement task"""
    nrq.write('INIT:CONT OFF') # Switch of continuous measurement
    nrq.write('SENS:FUNC "XTIM:POW"')  # Change acquisition mode to trace measurement
    nrq.write('SENS:FREQ 1.000000e+009')  # Set measurement frequency
    nrq.write('UNIT:POWer DBM')  # Get all the results in dBm (is W as standard after preset)
    nrq.query_opc()

    # Trace time is more or less the same as aperture time in that case.
    # However, the difference is, that we have to take care about the combination of trace time and the number of
    # trace points to avoid decimation. The acquisition sample rate of the NRQ6 is specified to a maximum of 121 MHz.
    # This means that it is automatically selected by the instrument. We request the current acquisition sample rate
    # and calculate the according time frame in respect to the number of samples.
    sr = nrq.query_float('SENSe1:BANDwidth:SRATe?')  # Request current sample rate
    aperture = 1 / sr * samples  # Calculate the measurement time (aperture) for one measurement
    nrq.write(f'SENS:TRAC:POIN {samples}')  # Define number of trace points
    nrq.write(f'SENS:TRAC:TIME {aperture}') # Set measurement time frame
    nrq.write('TRIG:SOUR IMMediate')  # Measures immediately, does not wait for a trigger condition
    nrq.write('SENS:TRACE:AVER:COUN 1')  # Single shot, at the end no averaging
    nrq.query_opc()


def measurement():
    # Perform the measurement and print the result
    nrq.write('FORM ASCii')  # Get the result in ASCII format
    nrq.write('INIT:IMM')  # Initiate a trigger
    trace_data = nrq.query_bin_or_ascii_float_list('FETC?')  # Query trace data into a list
    print()
    print(f'The Peak value is {max(trace_data):.3f} dBm')
    print(f'The Average value is {sum(trace_data)/len(trace_data):.3f} dBm')
    print(f'The Sample (first) value is {trace_data[0]:.3f} dBm')


# Main Program begins here
com_prep()
com_check()
meas_setup()
measurement()
close()
