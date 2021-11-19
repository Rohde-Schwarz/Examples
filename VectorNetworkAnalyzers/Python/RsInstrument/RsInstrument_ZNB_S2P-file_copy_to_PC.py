"""
# github examples repository path: VectorNetworkAnalyzers/Python/RsInstrument

Created 2021/05

Author:                     Jahns_P
Version Number:             1
Date of last change:        2021/06/01
Requires:                   R&S ZNB, FW 3.12 or newer and adequate options
                            Installed VISA e.g. R&S Visa 5.12.x or newer

Description:    Example for remote calibration with robot support to feed the calibration elements.


General Information:

Please always check this example script for unsuitable setting that may
destroy your DUT before connecting it to the instrument!
This example does not claim to be complete. All information has been compiled with care.
However, errors can not be ruled out.

Please find more information about RsInstrument at
https://rsinstrument.readthedocs.io/en/latest/
"""


from RsInstrument import *
from time import sleep

# Define variables
resource = 'TCPIP0::10.205.0.172::INSTR'                                                  # VISA resource string for the device
s2p_filename = r'C:\Users\Public\Documents\Rohde-Schwarz\Vna\Traces\s2pfile.s2p'          # Name and path of the s2p file on the instrument
pc_filename = r'C:\Tempdata\pcs2pfile.s2p'                                                # Name and path of the s2p file on the PC


# Make sure you have the last version of the RsInstrument
RsInstrument.assert_minimum_version('1.19.0.75')

# Define the device handle
# Instrument = RsInstrument(resource)
Instrument = RsInstrument(resource, True, True, "SelectVisa='rs'")
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
sleep(1)                                                                              # Eventually add some waiting time when reset is performed during initialization


def comprep():
    """Preparation of the communication (termination, etc...)"""
    print(f'VISA Manufacturer: {Instrument.visa_manufacturer}')     # Confirm VISA package to be chosen
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
    # RF Setup first
    Instrument.write_str_with_opc('SYSTEM:DISPLAY:UPDATE ON')                                       # Be sure to have the display updated whilst remote control
    Instrument.write_str_with_opc('SENSe1:FREQuency:Start 700e6')                                   # Set start frequency to 700 MHz
    Instrument.write_str_with_opc('SENSe1:FREQuency:Stop 1.3e9')                                    # Set stop frequency to 1.3 GHz
    Instrument.write_str_with_opc('SENSe1:SWEep:POINts 501')                                        # Set number of sweep points

    # Prepare S11 measurement in diagram 1
    Instrument.write_str_with_opc('CALCulate1:PARameter:MEAsure "Trc1", "S11"')                     # Change active trace to S11 measurement
    Instrument.write_str_with_opc('CALCulate1:Format MAGNitude')                                    # Be sure to have active trace's format to dB Mag
    Instrument.write_str_with_opc('CALCulate1:PARameter:SDEFine "Trc2", "S11"')                     # Add a second trace
    Instrument.write_str_with_opc('CALCulate1:Format PHASe')                                        # Change active trace's format to phase
    Instrument.write_str_with_opc('DISPlay:WINDow1:TRACe2:FEED "Trc2"')                             # Display the second trace

    # Prepare S22 measurement in diagram 2 like for S11 if not separately commented
    Instrument.write_str_with_opc('DISPlay:WINDow2:STATe ON')                                       # Add another diagram
    Instrument.write_str_with_opc('CALCulate1:PARameter:SDEFine "Trc3", "S22"')                     # Add a third trace
    Instrument.write_str_with_opc('CALCulate1:Format MAGNitude')
    Instrument.write_str_with_opc('DISPlay:WINDow2:TRACe3:FEED "Trc3"')
    Instrument.write_str_with_opc('CALCulate1:PARameter:SDEFine "Trc4", "S22"')
    Instrument.write_str_with_opc('CALCulate1:Format PHASe')
    Instrument.write_str_with_opc('DISPlay:WINDow2:TRACe4:FEED "Trc4"')

    # Prepare S21 measurement in diagram 3 like  before if not separately commented
    Instrument.write_str_with_opc('DISPlay:WINDow3:STATe ON')
    Instrument.write_str_with_opc('CALCulate1:PARameter:SDEFine "Trc5", "S21"')
    Instrument.write_str_with_opc('CALCulate1:Format MAGNitude')
    Instrument.write_str_with_opc('DISPlay:WINDow3:TRACe3:FEED "Trc5"')
    Instrument.write_str_with_opc('CALCulate1:PARameter:SDEFine "Trc6", "S21"')
    Instrument.write_str_with_opc('CALCulate1:Format PHASe')
    Instrument.write_str_with_opc('DISPlay:WINDow3:TRACe4:FEED "Trc6"')

    # Prepare S12 measurement in diagram 4 like  before if not separately commented
    Instrument.write_str_with_opc('DISPlay:WINDow4:STATe ON')
    Instrument.write_str_with_opc('CALCulate1:PARameter:SDEFine "Trc7", "S12"')
    Instrument.write_str_with_opc('CALCulate1:Format MAGNitude')
    Instrument.write_str_with_opc('DISPlay:WINDow4:TRACe3:FEED "Trc7"')
    Instrument.write_str_with_opc('CALCulate1:PARameter:SDEFine "Trc8", "S12"')
    Instrument.write_str_with_opc('CALCulate1:Format PHASe')
    Instrument.write_str_with_opc('DISPlay:WINDow4:TRACe4:FEED "Trc8"')


def measure():
    """Perform a single sweep measurement"""
    Instrument.write_str_with_opc('INIT1:CONTinuous OFF')
    Instrument.write_str_with_opc('INIT1:IMMediate')


def saves2p():
    """Save the measurement to a s2p file"""
    Instrument.write_str_with_opc(f'MMEMory:STORe:TRACe:PORTs 1, "{s2p_filename}", COMPlex, 1, 2')
    # An S2P file does only contain real and imaginary part of each scatter parameter of the measurement.
    # To extract e.g. the magnitude and phase data of each trace, better use the command
    # MMEMory:STORe:TRACe:CHANnel 1, 'tracefile.csv', FORM, LINPhase
    # Using this simple file format it will be stored in path
    # C:\Users\Public\Documents\Rohde-Schwarz\Vna


def fileget():
    """Perform calibration with short element"""
    Instrument.read_file_from_instrument_to_pc(s2p_filename, pc_filename)


# ---------------------------
# Main Program begins here
# just calling the functions
# ---------------------------

comprep()
comcheck()
meassetup()
measure()
saves2p()
fileget()
close()

print('I am done')
