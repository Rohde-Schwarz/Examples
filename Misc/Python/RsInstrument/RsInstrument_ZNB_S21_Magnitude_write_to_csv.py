"""

Created 2022/02

Author:                     Jahns_P
Version Number:             1
Date of last change:        2022/02/17
Requires:                   R&S ZNB, FW 3.12 or newer and adequate options
                            Installed VISA e.g. R&S Visa 5.12.x or newer

Description:    Example to measure S21 attenuation and write the results into a CSV file.


General Information:

Please always check this example script for unsuitable setting that may
destroy your DUT before connecting it to the instrument!
This example does not claim to be complete. All information has been
compiled with care. However, errors can not be ruled out.
"""

# --> Import necessary packets  
from RsInstrument import *
from time import sleep

# Define variables
resource = 'TCPIP0::10.205.0.51::INSTR'  # VISA resource string for the device
PcFile = r'c:\tempdata\logfile.CSV'  # Name and path of the logfile
points = 401  # Number of sweep points

# Define the device handle
# znb = RsInstrument(resource)
znb = RsInstrument(resource, True, True, "SelectVisa='rs'")
"""
(resource, True, True, "SelectVisa='rs'") has the following meaning:
(VISA-resource, id_query, reset, options)
- id_query: if True: the instrument's model name is verified against the models 
supported by the driver and eventually throws an exception.   
- reset: Resets the instrument (sends *RST) command and clears its status syb-system
- option SelectVisa:
			- 'SelectVisa = 'socket' - uses no VISA implementation for socket connections - you do not need any VISA-C installation
			- 'SelectVisa = 'rs' - forces usage of Rohde&Schwarz Visa
			- 'SelectVisa = 'ni' - forces usage of National Instruments Visa     
"""
sleep(1)  # Eventually add some waiting time when reset is performed during initialization


def com_prep():
    """Preparation of the communication (termination, etc...)"""

    print(f'VISA Manufacturer: {znb.visa_manufacturer}')  # Confirm VISA package to be chosen
    znb.visa_timeout = 5000  # Timeout for VISA Read Operations
    znb.opc_timeout = 5000  # Timeout for opc-synchronised operations
    znb.instrument_status_checking = True  # Error check after each command, can be True or False
    znb.clear_status()  # Clear status register


def close():
    """Close the VISA session"""

    znb.close()


def com_check():
    """Check communication with the device"""

    # Just knock on the door to see if instrument is present
    idnResponse = znb.query_str('*IDN?')
    sleep(1)
    print('Hello, I am ' + idnResponse)


def meas_setup():
    """Assign more detailed settings and segments to the channels"""
    #
    # Setup for CH1
    #
    znb.write_str('SENSe1:FREQuency:STARt 0.01GHZ')  # Start frequency to 10 MHz
    znb.write_str('SENSe1:FREQuency:STOP 1.0GHZ')  # Stop frequency to 1 GHz

    znb.write('SENSe1:SWEep:POINts ' + str(points))  # Set number of sweep points to the defined number
    znb.write_str('CALCulate1:PARameter:MEASure "Trc1", "S21"')  # Measurement now is S21
    sleep(0.5)  # It will take some time to perform a complete sweep - wait for it
    znb.write_str('DISPlay:WINDow1:TRACe1:Y:SCALe:AUTO ONCE')  # Enable auto scaling for trace 1
    znb.write_str_with_opc("INIT1:CONT OFF")  # Set single sweep mode and stop acquisition


def file_write():
    # open logfile
    logfile = open(PcFile, "w")
    # write table headline
    logfile.write("Frequ / Hz; Atten. / db")
    logfile.write("\n")
    points_count = znb.query_int('SENSe1:SWEep:POINts?')  # Request number of frequency points
    trace_data = znb.query_str('CALC1:DATA? FDAT')  # Get measurement values for complete trace
    trace_tup = tuple(map(str, trace_data.split(',')))  # Convert the received string into a tuple
    freq_list = znb.query_str('CALC:DATA:STIM?')  # Get frequency list for complete trace
    freq_tup = tuple(map(str, freq_list.split(',')))  # Convert the received string into a tuple

    # Now write frequency and magnitude for each point and close the file if done
    x = 0
    while x < points:
        logfile.write(freq_tup[x] + ";")
        logfile.write(trace_tup[x] + "\n")
        x = x + 1
    logfile.close()


# -------------------------------------------------------------------------
# Main Program begins here just calling the functions
# -------------------------------------------------------------------------


com_prep()
com_check()
meas_setup()
file_write()
close()

print()
print("I'm done. Data is written to ", PcFile)
