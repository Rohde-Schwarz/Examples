"""
# GitHub examples repository path: VectorNetworkAnalyzers/Python/RsInstrument

Created 2021/11

Author:                     Jahns_P
Version Number:             1
Date of last change:        2021/11/08
Requires:                   R&S ZNB, FW 3.12 or newer and adequate options
                            Installed VISA e.g. R&S Visa 5.12.x or newer

Description:    Example for ZNx segmented sweep performed on one channel


General Information:

Please always check this example script for unsuitable setting that may
destroy your DUT befor connecting it to the instrument!
This example does not claim to be complete. All information has been
compiled with care. However, errors can not be ruled out.
"""

from RsInstrument import *
from time import sleep

# Define variables
resource = 'TCPIP::10.102.73.16::hislip0'                                                  # VISA resource string for the device

# Make sure you have the last version of the RsInstrument
RsInstrument.assert_minimum_version('1.53.0')

# Define the device handle
# Instrument = RsInstrument(resource)
io = RsInstrument(resource, True, True, "SelectVisa='rs'")
'''
(resource, True, True, "SelectVisa='rs'") has the following meaning:
(VISA-resource, id_query, reset, options)
- id_query: if True: the instrument's model name is verified against the models 
supported by the driver and eventually throws an exception.   
- reset: Resets the instrument (sends *RST) command and clears its status syb-system
- option SelectVisa:
            - 'SelectVisa = 'socket' - uses no VISA implementation for socket connections - you do not need any VISA-C installation
            - 'SelectVisa = 'rs' - forces usage of Rohde&Schwarz Visa
            - 'SelectVisa = 'ni' - forces usage of National Instruments Visa     
'''
sleep(1)                                                                              # Eventually add some waiting time when reset is performed during initialization


def comprep():
    """Preparation of the communication (termination, etc...)"""

    print(f'VISA Manufacturer: {io.visa_manufacturer}')     # Confirm VISA package to be chosen
    io.visa_timeout = 5000                                  # Timeout for VISA Read Operations
    io.opc_timeout = 5000                                   # Timeout for opc-synchronised operations
    io.instrument_status_checking = True                    # Error check after each command, can be True or False
    io.clear_status()                                       # Clear status register


def close():
    """Close the VISA session"""

    io.close()


def comcheck():
    """Check communication with the device"""

    # Just knock on the door to see if instrument is present
    idnResponse = io.query_str('*IDN?')
    sleep(1)
    print('Hello, I am ' + idnResponse)


def meassetup():
    """Prepare measurement setup for two segments measuring in channel 1 and trace 1"""

    # RF Setup first
    io.write_with_opc('SYSTEM:DISPLAY:UPDATE ON')                                       # Be sure to have the display updated whilst remote control
    io.write_with_opc('INIT:CONT OFF')                                                  # Set single sweep mode
    io.write_with_opc('SENSe:SWEep:TIME:AUTO ON')                                       # Auto Sweep time
    io.write_with_opc('TRIGger:SEQuence:SOURce IMMediate')                              # Trigger immediate (Auto)
    io.write_with_opc('AVERage OFF')                                                    # Averaging disabled
    io.write_with_opc('SEGment:CLEar')                                                  # Deletes all sweep segments in the channel

    #
    # Define Segment 1 for CH1
    #

    # Ch1 Trc1 already exists by default
    io.write_with_opc("CALCULATE1:PARAMETER:SDEFINE 'Trc1', 'S22'")                     # Reconfigure the trace Trc1 to S22
    io.write_with_opc("DISPLAY:WINDOW1:TRACE:EFEED 'Trc1'")                             # Feed it again to the window

    io.write_with_opc("SENSe1:SEGMent1:ADD")                                            # Add Segment 1
    io.write_with_opc("SENSe1:SEGMent1:FREQuency:STARt 500MHz")                         # Start Frequency
    io.write_with_opc("SENSe1:SEGMent1:FREQuency:STOP 900MHz")                          # Stop Frequency
    io.write_with_opc("SENSe1:SEGMent1:SWEep:POINts 401")                               # No of Sweep Points
    io.write_with_opc("SENSe1:SEGMent1:POWer:LEVel 10")                                 # Output Power Level
    io.write_with_opc("SENSe1:SEGMent1:BWIDth 500Hz")                                   # RBW

    #
    # Define Segment 2 for CH1
    #
    # Using the complete command including "SENSe" will define the channel the changes will be associated to
    io.write_with_opc("SENSe1:SEGMent2:ADD")                                            # Add Segment 2
    io.write_with_opc("SENSe1:SEGMent2:FREQuency:STARt 1200MHz")                        # Start Frequency
    io.write_with_opc("SENSe1:SEGMent2:FREQuency:STOP 2400MHz")                         # Stop Frequency
    io.write_with_opc("SENSe1:SEGMent2:SWEep:POINts 501")                               # No of Sweep Points
    io.write_with_opc("SENSe1:SEGMent2:POWer:LEVel 0")                                  # Output Power Level
    io.write_with_opc("SENSe1:SEGMent2:BWIDth 1000Hz")                                  # RBW


def measure():
    """ Initiate sweep and capture measurement data"""
    io.write_with_opc('SWEep:TYPE SEGMent')                                             # Segmented sweep mode
    io.write_with_opc('INIT')

    #
    # Add markers and get the results for CH1
    #
    io.write_with_opc("CALCulate1:MARKer1:STATe ON")  # Activate Marker 1
    io.write_with_opc("CALCulate1:Marker1:FUNCtion:EXECute MINimum")  # Assign Minimum Function to Marker 1
    res_mark1_min = io.query_str("CALCulate1:MARKer1:FUNCtion:RESult?")  # Read the result X,Y
    print(f"Result for CH1 Marker 1 (maximum) is: {res_mark1_min} dB")

    io.write_with_opc("CALCulate1:MARKer2:STATe ON")  # Activate Marker 2
    io.write_with_opc("CALCulate1:Marker2:FUNCtion:EXECute MAXimum")  # Assign Maximum Function to Marker 2
    res_mark2_max = io.query_str("CALCulate1:MARKer2:FUNCtion:RESult?")  # Read the result
    print(f"Result for CH1 Marker 2 (minimum) is: {res_mark2_max} dB")

    io.write_with_opc("CALCulate1:MARKer3:STATe ON")  # Activate Marker 3
    io.write_with_opc("CALCulate1:Marker3:X 2 GHz")  # Set to a dedicated Frequency
    res_mark3_freq = io.query_float(f"CALCulate1:MARKer3:Y?")  # Read the Y result
    print(f"Result for CH1 Marker 3 on 2 GHz is: {res_mark3_freq:0.3f} dB")

    #
    # Get Trace Data for CH1
    #

    data = io.query_bin_or_ascii_float_list("FORM REAL,32;CALCulate1:DATA? SDATa")
    print("CH1 Trace Result Data is: ", data)


# ---------------------------
#  Main Program begins here
#  just calling the functions
# ---------------------------


comprep()
comcheck()
meassetup()
measure()
close()


print("I'm done")
