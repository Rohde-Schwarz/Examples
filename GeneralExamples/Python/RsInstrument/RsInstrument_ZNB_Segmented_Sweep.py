"""

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
compiled with care. However errors can not be ruled out.
"""

# --> Import necessary packets  
from RsInstrument import *
from time import sleep

# Define variables
resource = 'TCPIP0::10.205.0.51::INSTR'                                                  # VISA resource string for the device


# Define the device handle
# Instrument = RsInstrument(resource)
Instrument = RsInstrument(resource, True, True, "SelectVisa='rs'")
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

    print(f'VISA Manufacturer: {Instrument.visa_manufacturer}')     # Confirm VISA package to be choosen
    Instrument.visa_timeout = 5000                                  # Timeout for VISA Read Operations
    Instrument.opc_timeout = 5000                                   # Timeout for opc-synchronised operations
    Instrument.instrument_status_checking = True                    # Error check after each command, can be True or False
    Instrument.clear_status()                                       # Clear status register


def close():
    """Close the VISA session"""

    Instrument.close()


def comcheck():
    """Check communication with the device"""

    # Just knock on the door to see if instrument is present
    idnResponse = Instrument.query_str('*IDN?')
    sleep(1)
    print('Hello, I am ' + idnResponse)


def meassetup():
    """Prepare measurement setup for two segments measuring in channel 1 and trace 1"""

    # RF Setup first
    Instrument.write_str_with_opc('SYSTEM:DISPLAY:UPDATE ON')                                       # Be sure to have the display updated whilst remote control
    Instrument.write_str_with_opc('INIT:CONT OFF')                                                  # Set single sweep mode
    Instrument.write_str_with_opc('SENSe:SWEep:TIME:AUTO ON')                                       # Auto Sweep time
    Instrument.write_str_with_opc('TRIGger:SEQuence:SOURce IMMediate')                              # Trigger immediate (Auto)
    Instrument.write_str_with_opc('AVERage OFF')                                                    # Averaging disabled
    Instrument.write_str_with_opc('SEGment:CLEar')                                                  # Deletes all sweep segments in the channel
    Instrument.write_str_with_opc('FREQuency:MODE SEGMent')                                         # Change mode to frequency segmented operations

    #
    # Define Segment 1
    #
    Instrument.write_str_with_opc('SEGMent1:ADD')                                                   # Add Segment 1
    Instrument.write_str_with_opc('SEGMent1:FREQuency:STARt 500MHz')                                # Start Frequency
    Instrument.write_str_with_opc('SEGMent1:FREQuency:STOP 900MHz')                                 # Stop Frequency
    Instrument.write_str_with_opc('SEGMent1:SWEep:POINts 401')                                      # No of Sweep Points
    Instrument.write_str_with_opc('SEGMent1:POWer:LEVel 10')                                        # Output Power Level
    Instrument.write_str_with_opc('SEGMent1:BWIDth 500Hz')                                          # RBW

    #
    # Define Segment 2
    #
    Instrument.write_str_with_opc('SEGMent2:ADD')                                                   # Add Segment 2
    Instrument.write_str_with_opc('SEGMent2:FREQuency:STARt 1200MHz')                               # Start Frequency
    Instrument.write_str_with_opc('SEGMent2:FREQuency:STOP 2400MHz')                                # Stop Frequency
    Instrument.write_str_with_opc('SEGMent2:SWEep:POINts 501')                                      # No of Sweep Points
    Instrument.write_str_with_opc('SEGMent2:POWer:LEVel 0')                                         # Output Power Level
    Instrument.write_str_with_opc('SEGMent2:BWIDth 1000Hz')                                         # RBW


def measure():
    """ Initiate sweep and capture measurement data"""
    Instrument.write_str_with_opc('INIT')
    data = Instrument.query_str('CALCulate:DATA? SDATa')
    print(data)


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
