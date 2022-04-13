"""

Created on 2022/04

Author: Jahns_P
Version Number: 1
Date of last change: 2022/04/11
Requires: FPC1x00 series SPA, FW 1.70 or newer and adequate options
- Installed RsInstrument Python module 1.70 or newer
- Installed VISA e.g. R&S Visa 5.12.x or newer

Description: Setup measurement, get trace data, slice it, calculate frequency list, and save data to a local CSV file


General Information:

Please always check this example script for unsuitable setting that may
destroy your DUT before connecting it to the instrument!
This example does not claim to be complete. All information has been
compiled with care. However, errors can not be ruled out.

Please find more information about RsInstrument at
https://rsinstrument.readthedocs.io/en/latest/
"""

# --> Import necessary packets
from RsInstrument import *
from time import sleep

# Define variables
resource = 'TCPIP::10.205.0.184::INSTR'  # VISA resource string for the device
# resource = 'TCPIP::172.16.10.10::INSTR'  # Original resource string when using USB connection
recdur = 10  # Time in seconds to find max hold peaks
filename = r'C:\test\TraceFile.CSV'

# Define the device handle
instrument = RsInstrument(resource, reset=True, id_query=True, options="SelectVisa='rs'")
'''
- option SelectVisa:
    - 'SelectVisa = 'socket' - uses no VISA implementation for socket connections 
                             - you do not need any VISA-C installation
    - 'SelectVisa = 'rs' - forces usage of Rohde&Schwarz Visa
    - 'SelectVisa = 'ni' - forces usage of National Instruments Visa     
'''


#
# Define subroutines
#


def com_prep():
    """Preparation of the communication (termination, timeout, etc...)"""
    
    print(f'VISA Manufacturer: {instrument.visa_manufacturer}')  # Confirm VISA package to be chosen
    instrument.visa_timeout = 5000  # Timeout in ms for VISA Read Operations
    instrument.opc_timeout = 3000  # Timeout in ms for opc-synchronised operations
    instrument.instrument_status_checking = True  # Error check after each command
    instrument.clear_status()  # Clear status register
  
    
def close():
    """Close the VISA session"""
    instrument.close()


def com_check():
    """Check communication with the device by requesting it's ID"""
    idn_response = instrument.query_str('*IDN?')
    print('Hello, I am ' + idn_response)
    
   
def meas_prep():
    """Prepare instrument for desired measurements
    In this case
    - Set Center Frequency to 1540 MHz
    - Set Span to 100 MHz
    - Set Trace to Max Hold (and Positive Peak automatically)
    """

    instrument.write_str_with_opc('FREQuency:CENTer 2450e6')  # Center Frequency to 2450 MHz
    instrument.write_str_with_opc('FREQuency:SPAN 100e6')  # SPAN is 100 MHz now
    instrument.write_str_with_opc('DISPlay:TRACe1:MODE MAXHold')  # Trace to Max Hold


def trace_get():
    """Initialize continuous measurement, stop it after the desired time, query trace data"""

    instrument.write_str_with_opc('INITiate:CONTinuous ON')  # Continuous measurement on trace 1 ON
    print('Please wait for maxima to be found...')
    sleep(int(recdur))  # Wait for preset record time
    instrument.write('INITiate:CONTinuous OFF')  # Continuous measurement on trace 1 OFF
    instrument.query_opc()
    sleep(0.5)

    # Get y data (amplitude for each point)
    trace_data = instrument.query('Trace:DATA? TRACe1')  # Read y data of trace 1
    csv_trace_data = trace_data.split(",")  # Slice the amplitude list
    trace_len = len(csv_trace_data)  # Get number of elements of this list

    # Reconstruct x data (frequency for each point) as it can not be directly read from the instrument
    start_freq = instrument.query_float('FREQuency:STARt?')
    span = instrument.query_float('FREQuency:SPAN?')
    step_size = span / (trace_len-1)

    # Now write values into file
    file = open(filename, 'w')  # Open file for writing
    file.write("Frequency in Hz;Power in dBm\n")  # Write the headline
    x = 0  # Set counter to 0 as list starts with 0
    while x < int(trace_len):  # Perform loop until all sweep points are covered
        file.write(f'{(start_freq + x * step_size):.1f}')  # Write adequate frequency information
        file.write(";")
        amp = float(csv_trace_data[x])
        file.write(f'{amp:.2f}')  # Write adequate amplitude information
        file.write("\n")
        x = x+1
    file.close()  # CLose the file
    
#
# -------------------------
# Main Program begins here
# -------------------------
#
    

com_prep()
com_check()
meas_prep()
trace_get()
close()


print('Program successfully ended.')
print('Wrote trace data into', filename)
