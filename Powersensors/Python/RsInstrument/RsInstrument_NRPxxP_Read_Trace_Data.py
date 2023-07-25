"""
Created 2023/07

Author:                     Winfried Jansen
Version Number:             1
Date of last change:        2023/07/21
Requires:                   R&S nrp_p, FW 1.10 or newer
                            Installed VISA e.g. R&S Visa 7.2.x or newer

Description: Example for NRPxxP sensors - measuring and querying the instrument trace data.


General Information:

Please always check this example script for unsuitable setting that may
destroy your DUT before connecting it to the instrument!
This example does not claim to be complete. All information has been
compiled with care. However, errors can not be ruled out.
"""

from RsInstrument import *
import numpy as np
import matplotlib.pyplot as plt
from time import *

# Define variables
resource = 'USB::0x0AAD::0x014E::900051::INSTR'  # VISA resource string for the device
global data_trace, y_val

# Make sure you have the last version of the RsInstrument
RsInstrument.assert_minimum_version('1.54.0')

# Define the device handle
try:
    nrp = RsInstrument(resource, reset=False, id_query=False, options="SelectVisa='rs'")
    nrp.visa_timeout = 3000  # Timeout for VISA Read Operations
    nrp.instrument_status_checking = True  # Error check after each command
except ResourceError as ex:
    print('Error initializing the instrument session:\n' + ex.args[0])
    exit()


def com_prep():
    """Preparation of the communication (termination, etc...)"""
    print(f'VISA Manufacturer: {nrp.visa_manufacturer}')  # Confirm VISA package to be chosen
    nrp.visa_timeout = 5000  # Timeout for VISA Read Operations
    nrp.opc_timeout = 5000  # Timeout for opc-synchronised operations
    nrp.instrument_status_checking = True  # Error check after each command, can be True or False
    nrp.clear_status()  # Clear status register


def close():
    """Close the VISA session"""
    nrp.close()


def com_check():
    """Check communication with the device"""
    # Just knock on the door to see if instrument is present
    print('Hello, I am ' + nrp.idn_string)
    if not nrp.full_instrument_model_name.endswith('P'):
        raise ValueError(f'Instrument "{nrp.full_instrument_model_name}" is not a pulse-power sensor. This example only works with NRP-xxP power sensors.')


def meas_setup():
    global y_val
    # Reset
    nrp.write_with_opc("*RST;*CLS")
    # Single sweep
    nrp.write("INIT:CONT OFF")
    # Trace function
    nrp.write("SENS:FUNC 'XTIM:POW'")
    # Frequency
    nrp.write("SENS:FREQ 1.000000e+009")
    # Trace points
    nrp.write("SENS:TRAC:POIN 500")
    number_points = nrp.query_int('SENS:TRAC:POIN?')
    # Trace length
    nrp.write('SENS:TRAC:TIME 10e-6')
    trace_length_s = nrp.query_float('SENS:TRAC:TIME?')
    # Trace offset time
    nrp.write_with_opc("SENS:TRAC:OFFS:TIME 0")
    y_val = np.linspace(0, trace_length_s, number_points)


def trig_setup():
    # Trigger settings
    nrp.write("TRIG:ATR:STAT OFF")
    nrp.write("TRIG:SOUR INT")
    nrp.write("TRIG:LEV 10e-6")
    nrp.write("TRIG:SLOP POS")
    nrp.write("TRIG:COUN 1")
    nrp.write("TRIG:DELay -10e-6")
    nrp.write("TRIGger:HYSTeresis 0.5")
    nrp.write("TRIGger:DTIME 0")
    nrp.write_with_opc("TRIG:Hold 0")


def aver_setup():
    # averaging settings
    nrp.write("SENS:TRACE:AVER:COUN 8")
    nrp.write("SENS:TRACE:AVER:STAT ON")
    nrp.write("SENS:TRACE:AVER:TCON REP")
    nrp.write("SENS:AVER:RES")
    nrp.write("SENS:TRACE:REAL OFF")
    nrp.write_with_opc("SENS:TRACE:MEAS:STAT OFF")


def measurement():
    # Initiate a measurement
    nrp.write("FORM REAL,32")
    nrp.write("FORM:BORD NORM")
    nrp.write("STAT:OPER:MEAS:NTR 2")
    nrp.write("STAT:OPER:MEAS:PTR 0")
    nrp.write("STAT:OPER:TRIG:NTR 2")
    nrp.write("STAT:OPER:TRIG:PTR 0")
    nrp.write("INIT:IMM")


def end_meas():
    # Waiting for the end of the measurement
    n = 0
    while n < 2:
        n = nrp.query_int('STAT:OPER:MEAS:EVEN?')
        sleep(0.010)


def get_res():
    # Get the result
    global data_trace
    data_trace = nrp.query_bin_or_ascii_float_list('FETC?')


def plot():
    # Plot the results
    global y_val
    global data_trace
    plt.plot(y_val, data_trace)
    plt.ylabel('power / W')
    plt.xlabel('time / us')
    plt.show()


# ---------------------------
# Main Program begins here
# just calling the functions
# ---------------------------
com_prep()
com_check()
meas_setup()
trig_setup()
aver_setup()
measurement()
end_meas()
get_res()
close()
plot()
