"""
# GitHub examples repository path: VectorNetworkAnalyzers/Python/RsInstrument
Created 2022/06

Author:                     Jahns_P
Version Number:             2
Date of last change:        2022/06/07
Requires:                   R&S zna, FW 3.40 or newer and adequate options
                            Installed VISA e.g. R&S Visa 5.12.x or newer

Description: Example for remote calibration including power calibration using an external auto-cal unit and power meter.


General Information:

Please always check this example script for unsuitable setting that may
destroy your DUT before connecting it to the instrument!
This example does not claim to be complete. All information has been
compiled with care. However, errors can not be ruled out.
"""

from RsInstrument import *
from time import sleep

# Define variables
resource = 'TCPIP0::10.205.0.60::INSTR'  # VISA resource string for the device

# Make sure you have the last version of the RsInstrument
RsInstrument.assert_minimum_version('1.53.0')

# Define the device handle
# zna = RsInstrument(resource)

zna = RsInstrument(resource, reset=True, id_query=True,
                   options="SelectVisa='rs' , LoggingMode = Off, LoggingToConsole = False")
'''
- option SelectVisa:
"SelectVisa = 'socket'" - uses no VISA implementation for socket connections - you do not need any VISA-C installation
"SelectVisa = 'rs'" - forces usage of Rohde&Schwarz Visa
"SelectVisa = 'ni'" - forces usage of National Instruments Visa     
'''


def comprep():
    """Preparation of the communication (termination, etc...)"""

    print(f'VISA Manufacturer: {zna.visa_manufacturer}')  # Confirm VISA package to be chosen
    zna.visa_timeout = 5000  # Timeout for VISA Read Operations
    zna.opc_timeout = 5000  # Timeout for opc-synchronised operations
    zna.instrument_status_checking = True  # Error check after each command, can be True or False
    zna.clear_status()  # Clear status register


def close():
    """Close the VISA session"""

    zna.close()


def comcheck():
    """Check communication with the device"""

    # Just knock on the door to see if instrument is present
    response = zna.query_str('*IDN?')
    sleep(1)
    print('Hello, I am ' + response)


def meassetup():
    """Prepare measurement setup"""
    # RF Setup first
    zna.write_str_with_opc('SYSTEM:DISPLAY:UPDATE ON')  # Be sure to have the display updated whilst remote control
    zna.write_str_with_opc('SENSe1:FREQuency:Start 1e9')  # Set start frequency to 1 GHz
    zna.write_str_with_opc('SENSe1:FREQuency:Stop 2e9')  # Set stop frequency to 2 GHz
    zna.write_str_with_opc('SENSe1:SWEep:POINts 501')  # Set number of sweep points
    zna.write_str_with_opc('CALCulate1:PARameter:MEAsure "Trc1", "S11"')  # Change active trace to S11 measurement

    zna.write_str('CALCulate1:PARameter:SDEFine "Ch1Tr2", "S21"')  # Define 2nd trace (S21) in 1st window / CH1
    zna.write_str('DISPlay:WINDow1:TRACe2:FEED "CH1TR2"')  # Display the new trace

    zna.write_str("CALCULATE2:PARAMETER:SDEFINE 'Trc21', 'S22'")  # Define a new trace (S22)in a 2nd window / CH2
    zna.write_str("DISPLAY:WINDOW2:STATE ON")  # Activate the new window
    zna.write_str("DISPLAY:WINDOW2:TRACE1:FEED 'Trc21'")  # And display the new trace

    zna.write_str('CALCulate2:PARameter:SDEFine "Ch2Tr2", "S12"')  # Define 2nd trace (S12) in 2nd window / CH2
    zna.write_str('DISPlay:WINDow2:TRACe2:FEED "CH2TR2"')  # Display the new trace

    zna.query_opc()  # check for command completion at the end of the command row

    sleep(1)  # wait for the display to be ready
    zna.write_str_with_opc('DISPlay:WINDow1:TRACe2:Y:SCALe:AUTO ONCE')  # Auto scale trace 2 in 1st window
    zna.write_str('INIT1:CONTinuous OFF')  # Initiate a single sweep for CH1 in window 1
    zna.write_str('INIT2:CONTinuous OFF')  # And do the same for the 2nd window / channel


def powcal():
    zna.write('SOURce1:POWer1:CORRection:COLLect:FLATness 1')  # Enables the source power calibration
    zna.write('SOURce1:POWer1:CORRection:COLLect:RRECeiver 1')  # Enable Reference receiver calibration together
    #                                                             with the source power calibration
    zna.visa_timeout = 30000  # Change timeouts as zna will take more than 15 - 20 seconds for the next operation
    zna.opc_timeout = 30000

    zna.write('SOURce1:POWer1:CORRection:PSELect PPOWer')  # Defines how to define the source power the R&S ZNA uses to
    #                                                        perform the first calibration sweep of the source power
    #                                                        calibration (Reference Receiver Cal Power).
    zna.write('SOURce1:POWer1:CORRection:PPOWer -10')  # Defines the source power the R&S ZNA uses to perform the first
    #                                                    calibration sweep of the source power calibration
    zna.write('SOURce:POWer:CORRection:COLLect:AVERage:NTOLerance 0.05 ')  # Set a tolerance level for power cal

    print('\n Please connect the power meter to port 1 and confirm')
    _ = input()
    zna.write('SOURce1:POWer1:CORRection:ACQuire Port,1')  # Perform a complete power calibration on port 1
    # And check the calibration result concerning success and max. deviation
    print(zna.query_str('SOURce1:POWer1:CORRection:ACQuire:VERification:RESult?'))

    zna.write('SOURce2:POWer2:CORRection:PSELect PPOWer')  # Defines how to define the source power the R&S ZNA uses to
    #                                                        perform the first calibration sweep of the source power
    #                                                        calibration (Reference Receiver Cal Power).
    zna.write('SOURce2:POWer2:CORRection:PPOWer -10')  # Defines the source power the R&S ZNA uses to perform the first
    #                                                    calibration sweep of the source power calibration

    print('\n Please change the power meter to port 2 now and confirm')
    _ = input()
    zna.write('SOURce2:POWer2:CORRection:ACQuire Port,2')  # Perform a complete power calibration on port 1
    # And check the calibration result concerning success and max. deviation
    print(zna.query_str('SOURce2:POWer2:CORRection:ACQuire:VERification:RESult?'))

    zna.opc_timeout = 5000  # Change back timeouts to standard values
    zna.visa_timeout = 5000


def cal():
    print('\n Please connect both ports to the adequate connectors of the cal unit and confirm')
    _ = input()
    zna.opc_timeout = 15000  # The calibration will take more than the 5 seconds of OPC timeout that is set as standard
    print('Now starting automatic calibration')
    zna.write_str_with_opc('SENSe1:CORRection:COLLect:AUTO:TYPE FNPort," ",1,2')  # Perform auto calibration using UOSM
    # Information (copied from the ZNA manual):
    # --> TOSM
    # Full n-port calibration with characterized Through.
    # If the selected cal unit characterization does not contain a Through characterization, the command silently falls
    # back to a FNPort (UOSM) calibration.
    print('Automatic calibration is done')
    zna.opc_timeout = 5000  # Set back OPC timeout to standard


def savecal():
    """Apply calibration after it is finished and save the calibration file"""
    sleep(2)
    zna.write_str_with_opc('MMEMORY:STORE:CORRection 1, "AUTOCAL.cal"')  # Save current calibration
    zna.write_str_with_opc('MMEMORY:LOAD:CORRection 1, "AUTOCAL.cal"')  # And reload it (just to show the command)


# ---------------------------
# Main Program begins here
# just calling the functions
# ---------------------------

comprep()
comcheck()
meassetup()
powcal()
cal()
savecal()
close()

print("I'm done")
