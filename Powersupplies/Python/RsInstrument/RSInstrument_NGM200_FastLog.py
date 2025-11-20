"""
# GitHub examples repository path: Powersupplies/Python/RsInstrument

Created 2021/03

Author:                     P.Jahns, T.Lechner
Version Number:             2
Date of last change:        2025/11/17
Requires:                   R&S NGM20x Power Supply,  FW 03.034 or newer and adequate options
                            Installed VISA e.g. R&S Visa 5.12.x or newer

Description:    Example of Data Logging with the NGM via network using the fast log function.



General Information:

Use USB-TMC, TCP, HiSLIP or raw socket connection. USB-CDC and GPIB are too slow for the FastLog data rates.
Please always check this example script for unsuitable setting that may
destroy your DUT before connecting it to the instrument!
Set the instrument to default and set required voltage and current values before starting this program.
FastLog data is collected into an internal buffer in the instrument and provided on the remote control interface
in chunks every 250 ms, independent of the sample rate.
If the data is not picked up during the next 20 ms, it is overwritten in the buffer.
This example does not claim to be complete. All information has been
compiled with care. However, errors can not be ruled out.

Please find more information about RsInstrument at
https://rsinstrument.readthedocs.io/en/latest/
"""

from RsInstrument import *

from datetime import datetime
import time
import os

# Define variables
resource = 'TCPIP0::10.102.188.250::inst0::INSTR'  # VISA resource string for the device. Replace with resource string of your instrument!
sample_count = 0
duration = 10.01   #run FastLog for 10 seconds
output_file_name = 'result.csv'

# Make sure you have the last version of the RsInstrument
RsInstrument.assert_minimum_version('1.110.0')

# Define the device handle, force selection of R&S VISA if available. If not, fall back to default VISA
instr = RsInstrument(resource, True, True, "SelectVisa='rs'")
"""
Initializes new RsInstrument session. \n
Parameter options tokens examples:
- 'Simulate = True' - starts the session in simulation mode. Default: False
- 'SelectVisa = 'socket' - uses no VISA implementation for socket connections - you do not need any VISA-C installation
- 'SelectVisa = 'rs' - forces usage of Rohde&Schwarz Visa
- 'SelectVisa = 'ni' - forces usage of NI Visa
:param resource_name: VISA resource name, e.g. 'TCPIP::192.168.2.1::INSTR'
:param id_query: if True: the instrument's model name is verified against the models supported by the driver and eventually throws an exception
:param reset: Resets the instrument (sends *RST) command and clears its status syb-system
:param options: string tokens alternating the driver settings
:param direct_session: Another driver object or pyVisa object to reuse the session instead of opening a new session
"""

# Define all the subroutines


def bit_set(integer, bit_idx):
    return int(integer) & (1 << bit_idx)


def com_prep():
    """Preparation of the communication (termination, etc...)"""
    # this kind of format ensures to get the information shown in the docstrings
    try:
        print(f'VISA Manufacturer: {instr.visa_manufacturer}')  # Confirm VISA package to be chosen
        instr.visa_timeout = 3000  # Timeout for VISA Read Operations
        instr.opc_timeout = 3000  # Timeout for opc-synchronised operations
        instr.instrument_status_checking = True  # Error check after each command
        instr.opc_query_after_write = True  # *OPC? query after each write command
        instr.clear_status()  # Clear status register
    except Exception as ex:
        print('Error initializing the instrument session:\n' + ex.args[0])
        exit()

    print(f'Device IDN: {instr.idn_string}')
    print(f'Device Options: {",".join(instr.instrument_options)}')


def meas_prep():
    # Stop potentially running FastLog
    instr.write('FLOG:STATe 0')
    """Preparation of the measurement process"""
    instr.write('INST OUT1')  # Choose channel 1 for the following commands
    instr.write('OUTP:SEL 1')  # Activate the selected channel
    instr.write('OUTP:GEN 1')  # Activate Main Output

    instr.write('FLOG:SRATe S001k')  # Set logging speed (sample rate)
    # The following parameters are available to set the log sample rate:
    # S100 / S001k / S010k / S050k / S250k  / S500K
    instr.write('FLOG:TARGet SCPI')  # Redirect fast log data to SCPI port (Remote Control)


def init_flog():
    # Stop potentially running FastLog
    instr.write('FLOG:STATe 0')
    # Set fix current readback range. For available ranges see the instrument manual.
    instr.write('SENS:CURR:RANG 1')
    # Set up the status system
    instr.write('STATus:OPERation:ENABle 8192')
    instr.write('STATus:OPERation:PTRansition 8192')
    instr.write('STATus:OPERation:NTRansition 0')
    instr.write('STATus:OPERation:INST:ENABle 7')
    instr.write('STATus:OPERation:INST:PTRansition 7')
    instr.write('STATus:OPERation:INST:NTRansition 0')
    instr.write('STATus:OPERation:INST:ISUM1:ENABle 4096')
    instr.write('STATus:OPERation:INST:ISUM1:PTRansition 4096')
    instr.write('STATus:OPERation:INST:ISUM1:NTRansition 0')
    # Clear event registers of the status system by read operation (content is discarded)
    instr.query('STATus:OPERation:EVENt?')
    instr.query('STATus:OPERation:INST:EVENt?')
    instr.query('STATus:OPERation:INST:ISUM1:EVENt?')
    instr.query_opc()
    # Start FastLog
    instr.write(':FLOG:STATe 1')


def read_and_write_flog_data(file):
    """ Reads binary data from the instrument and saves it to the specified raw file.
    Data format is IEEE float. There is one voltage readback value and one current readback value per sample."""
    global sample_count
    instr.bin_float_numbers_format = BinFloatFormat.Single_4bytes  # Define binary format for conversion (4 Bytes means 32 bits)
    data = instr.query_bin_or_ascii_float_list('FLOG:DATA?')  # Read the binary block and convert it
    sample_count += int(len(data) / 2)
    for i in range(int(len(data) / 2)):
        idx_pair = i * 2
        out_str = str(data[idx_pair]) + ',' + str(data[idx_pair + 1]) + '\n'
        file.write(out_str + '\n')


def save_flog_data(file):
    
    # First the status system is queried whether new data is available
    stb = instr.query('*STB?')
    if not bit_set(stb, 7):
        return

    operation_register = instr.query(':STATus:OPERation:EVENt?')
    if not bit_set(operation_register, 13):
        return

    instRegister = instr.query(':STATus:OPERation:INST:EVENt?')
    if not bit_set(instRegister, 1):
        return

    instSumRegister = instr.query(':STATus:OPERation:INST:ISUM1:EVENt?')
    if not bit_set(instSumRegister, 12):
        return

    # Data is available. Query it from the instrument:
    read_and_write_flog_data(file)


def stop_flog():
    instr.write(':FLOG 0')
    instr.write(':OUTP 0')


def close():
    #Close the VISA session
    instr.close()


# --------------------------
# Main program begins here
# --------------------------

com_prep()
meas_prep()
init_flog()
output_file = open(output_file_name, "w+")
print("File location:", os.getcwd())
startTime = datetime.now()

def in_duration():
    timeDiff = datetime.now() - startTime
    elapsedTime = timeDiff.total_seconds()
    return elapsedTime < duration + 0.4     # allow some extra time for start of FastLog and delivery of the last data

while in_duration():
    save_flog_data(output_file)
    time.sleep(0.05)

save_flog_data(output_file)
stop_flog()
output_file.flush()
output_file.close()
close()

print(sample_count, " samples received")
print("Program successfully ended.")