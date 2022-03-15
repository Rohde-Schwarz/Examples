'''

Created 2021/05

Author:                     Jahns_P
Version Number:             1
Date of last change:        2021/10/08
Requires:                   R&S CMA180, FW 1.7.10.58 or newer and adequate options
                            Installed VISA e.g. R&S Visa 5.12.x or newer

Description:    Example for remote power measurements using the internal RF generator and analyzer at the RF COM port.
                So there is no cabling needed.
                Expert Mode, Signal generation, Signal finding with AM signal, Power measurements, Modulation switching

General Information:

Please always check this example script for unsuitable setting that may
destroy your DUT before connecting it to the instrument!
This example does not claim to be complete. All information has been
compiled with care. However errors can not be ruled out.

Please find more information about RsInstrument at
https://rsinstrument.readthedocs.io/en/latest/
'''

# --> Import necessary packets  
from RsInstrument import *
from time import sleep

# Predefine variables
resource = 'TCPIP0::10.205.0.30::INSTR'  # VISA resource string for the device

RsInstrument.assert_minimum_version('1.21.0.78')  # Ensure to use a dedicated minimum version of RsInstrument
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
sleep(1)  # Eventually add some waiting time when reset is performed during initialization


def comprep():
    """Preparation of the communication (termination, etc...)"""

    print(f'VISA Manufacturer: {Instrument.visa_manufacturer}')  # Confirm VISA package to be chosen
    Instrument.visa_timeout = 5000  # Timeout for VISA Read Operations
    Instrument.opc_timeout = 5000  # Timeout for opc-synchronised operations
    Instrument.instrument_status_checking = True  # Error check after each command, can be True or False
    Instrument.clear_status()  # Clear status register


def close():
    """Close the VISA session"""

    Instrument.close()


def comcheck():
    """Check communication with the device"""

    # Just knock on the door to see if instrument is present
    idnResponse = Instrument.query_str('*IDN?')
    sleep(1)
    print('Hello, I am ' + idnResponse)


def meas_setup():
    """Switch CMA to Expert Mode and prepare  for first measurement with AM 80% / 1 kHz"""
    Instrument.write_str_with_opc("SYSTem:DISPlay:UPDate ON")  # Be sure the display is not switched off in remote mode
    Instrument.write_str_with_opc("CONFigure:BASE:SCENario EXPert")  # Switch to Expert Mode
    Instrument.write_str_with_opc("SOURce:AFRF:GEN:RFSettings:CONNector RFCom")  # Have the generator output switched to the RF COM port
    Instrument.write_str_with_opc("CONFigure:AFRF:MEAS:RFSettings:CONNector RFCom")  # Also switch the Analyzer input to the RF COM port
    Instrument.write_str_with_opc("SOURce:AFRF:GEN:RFSettings:FREQuency 145 MHz")  # Change generator frequency to 145 MHz
    Instrument.write_str_with_opc("SOURce:AFRF:GEN:RFSettings:LEVel -20")  # Set the (calculated) output level to -20 dBm
    # --> will lead to something like 20 dBm detected due to the attenuator being factored in
    Instrument.write_str_with_opc("SOURce:AFRF:GEN:MSCHeme AM")  # Modulation Scheme --> AM
    Instrument.write_str_with_opc("SOURce:AFRF:GEN:MODulator GEN3")  # Enable GEN3 as modulator (will be single tone / 1 kHz as standard after reset)
    Instrument.write_str_with_opc("SOURce:AFRF:GEN:MODulator:MDEPth 80")  # Set mod depth to 80 %
    Instrument.write_str_with_opc("SOURce:AFRF:GEN:STATe ON")  # Start signal transmission


def sigsearch():
    """Signal searching routine using the analyzer's "Find RF" routine"""
    Instrument.write_str_with_opc("CONFigure:AFRF:MEAS:FREQuency:COUNter:AUTomatic ON")  # Automatically switch analyzer to the detected frequency
    Instrument.write_str_with_opc("INITiate:AFRF:MEAS:FREQuency:COUNter")  # Start to find the signal (should be 145.000 MHz now)
    Freqread = Instrument.query_str("FETCh:AFRF:MEAS:FREQuency:COUNter?")  # Get frequency information
    Freqread = Freqread.split(",")  # Spilt the output into a List
    Freq = float(Freqread[1]) / 1000000
    print()
    print("Found a signal at " + str(Freq) + " MHz")


def measure():
    """Perform power measurements as predefined (AM/80%/1kHz) and compare with CW power measurement"""

    ###
    ### First Part: Perform the AM signal measurement
    ###

    # Instrument.write_str_with_opc("CONFigure:GPRF:MEAS:POWer:REPetition CONT")         # Set power measurement to repetitive mode does not work
    # as the CMA is always running in Single shot mode when driven via remote control.
    # It just can be preset for the case the unit gets back to local mode afterwards.
    Instrument.write_str_with_opc("INITiate:GPRF:MEAS:POWer")  # Initiate power measurement

    AvAM = Instrument.query_str("FETCh:GPRF:MEAS:POWer:CURRent?")  # Request Average Power
    AvAM = AvAM.split(",")  # Split the string as we get two values back
    print()
    print("The AM average power now is " + AvAM[1] + " dBm")  # Print value [1] (which is the second one)

    PkAM = Instrument.query_str("FETCh:GPRF:MEAS:POWer:MAXimum:CURRent?")  # Request Peak Power
    PkAM = PkAM.split(",")  # Split the string as we get two values back
    print("The AM peak power now is " + PkAM[1] + " dBm")  # Print value [1] (which is the second one)

    ###
    ### Second Part: Perform the CW signal measurement (Power measurement ist still active)
    ###

    Instrument.write_str_with_opc("SOURce:AFRF:GEN:MSCHeme CW")  # Modulation Scheme --> CW
    Instrument.write_str_with_opc("INITiate:GPRF:MEAS:POWer")  # Initiate power measurement

    AvCW = Instrument.query_str("FETCh:GPRF:MEAS:POWer:CURRent?")  # Request Average Power
    AvCW = AvCW.split(",")  # Split the string as we get two values back
    print("The CW average power now is " + AvCW[1] + " dBm")  # Print value [1] (which is the second one)

    ###
    ### Third Part: Compare Am to CW measurements
    ### The difference between CW and AM (@ 80% modulation depth) should be:
    ### 1.2 dB for average and 5,1 dB for peak
    ### (Conversion rate peak power AM vs CW = 10 * log ((1+m)*(1+m)) = 5.1 dB @ 80 % )
    ### (Conversion rate RMS power AM vs CW = 10 * log (1+m*m/2) = 1.2 dB @ 80 % )
    ###

    DiffAMavCW = float(AvAM[1]) - float(AvCW[1])  # Calculate Difference between AM average and CW Power
    print()
    print("Difference between CW and AM average is " + str(round(DiffAMavCW, 3)) + " dB")
    print("and should be about 1.2 dB")

    DiffAMpkCW = float(PkAM[1]) - float(AvCW[1])  # Calculate Difference between AM peak and CW power
    print()
    print("Difference between CW and AM peak is " + str(round(DiffAMpkCW, 3)) + " dB")
    print("and should be about 5,1 dB")


##
##---------------------------
## Main Program begins here
## just calling the functions
##---------------------------
##

comprep()
comcheck()
meas_setup()
sigsearch()
measure()
close()

print("I'm done")
