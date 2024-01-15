"""
# GitHub examples repository path: VectorNetworkAnalyzers/Python/RsInstrument
Created 2023/05

Author:                     Winfried Jansen
Version Number:             1
Date of last change:        2023/12/21
Requires:                   R&S ZNA, FW 2.90 or newer
                            or R&S ZNB, FW 3.50 or newer
                            or R&S ZVA, FW 4.11 or newer
                            Installed VISA e.g. R&S Visa 5.12.x or newer

Description: Example simultaneous measurement and readout of data.
We use 2 traces and 100 sweeps.
When one sweep is completed we get the trace data while the VNA runs the next sweep.


General Information:

Please always check this example script for unsuitable setting that may
destroy your DUT before connecting it to the instrument!
This example does not claim to be complete. All information has been
compiled with care. However, errors can not be ruled out.
"""

from RsInstrument import *

# Define variables
resource = 'TCPIP0::10.102.100.61::hislip0'  # VISA resource string for the device

# Make sure you have the last version of the RsInstrument
RsInstrument.assert_minimum_version('1.24.0')

# Define the device handle
vna = RsInstrument(resource, reset=True, id_query=True,
                   options="SelectVisa='rs' , LoggingMode = Off, LoggingToConsole = False")
'''
- option SelectVisa:
"SelectVisa = 'socket'" - uses no VISA implementation for socket connections - you do not need any VISA-C installation
"SelectVisa = 'rs'" - forces usage of Rohde & Schwarz Visa
"SelectVisa = 'ni'" - forces usage of National Instruments Visa     
'''


def com_prep():
    """Preparation of the communication (termination, etc...)"""
    print(f'VISA Manufacturer: {vna.visa_manufacturer}')  # Confirm VISA package to be chosen
    vna.visa_timeout = 5000  # Timeout for VISA Read Operations
    vna.opc_timeout = 5000  # Timeout for opc-synchronised operations
    vna.instrument_status_checking = True  # Error check after each command, can be True or False
    vna.clear_status()  # Clear status register


def close():
    """Close the VISA session"""
    vna.close()


def com_check():
    """Check communication with the device"""
    # Just knock on the door to see if instrument is present
    response = vna.query_str("*IDN?")
    print('Hello, I am ' + response)


def meas_setup():
    """Prepare measurement setup"""
    vna.write_str_with_opc("*RST")  # Reset
    vna.write_str_with_opc("SWE:POIN 5")  # Set sweep points to 5 only for testing
    vna.write_str_with_opc("CALC:PAR:SDEF 'Trc1','A1'")  # Switch to wave a1
    vna.write_str_with_opc("DISP:WIND:TRAC1:FEED 'Trc1'")  # Display the trace 1 in window 1
    vna.write_str_with_opc("CALC:PAR:SDEF 'Trc2','B1'")  # Switch on trace 2 with wave b1
    vna.write_str_with_opc("DISP:WIND:TRAC2:FEED 'Trc2'")  # Display the trace 2 in window 1
    vna.write_str_with_opc("INIT:CONT OFF")  # Switch to single sweep
    vna.write_str_with_opc("SENS:SWE:COUN 100")  # Set sweep count to 1000
    print(vna.query_str_with_opc("Syst:ERR?"))  # Check for errors
    vna.write_str("CALC:PAR:SEL 'Trc1'")  # select trace 1


def measurement():
    vna.write_str("INIT")  # Start the measurement
    for x in range(1, 100):
        y = x  # Set the start value
        while y <= x:  # In this loop one check if already the next sweep is running.
            # If yes we get the result from the sweep before
            y = int(vna.query_str("CALC:DATA:NSW:COUN?"))  # actual sweep number
            print(y, " ", x)  # only for testing
        vna.write_str("CALC:PAR:SEL 'Trc1'")  # select trace 1
        print(vna.query_str("CALC:DATA:NSW:FIRS? SDATA, " + str(x)))  # get the trace data
        vna.write_str("CALC:PAR:SEL 'Trc2'")  # select trace 2
        print(vna.query_str("CALC:DATA:NSW:FIRS? SDATA, " + str(x)))  # get the trace data
    # with the next part we get the last trace
    vna.write_str("CALC:PAR:SEL 'Trc1'")  # select trace 1
    print(vna.query_str("CALC:DATA:NSW:LAST? SDATA, 1"))  # get the trace data
    vna.write_str("CALC:PAR:SEL 'Trc2'")  # select trace 2
    print(vna.query_str("CALC:DATA:NSW:LAST? SDATA, 1"))  # get the trace data


# ---------------------------
# Main Program begins here
# just calling the functions
# ---------------------------

com_prep()
com_check()
meas_setup()
measurement()
close()

print("I'm done")
