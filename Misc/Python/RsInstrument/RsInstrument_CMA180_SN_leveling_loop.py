"""

Created 2022/04

Author:                     Jahns_P
Version Number:             2
Date of last change:        2022/04/11
Requires:                   R&S CMA180, FW 1.7.20 or newer and adequate options
                            Installed VISA e.g. R&S Visa 5.12.x or newer

Description:    Example about finding an adequate RF level to get a dedicated (S+N)/N value (20 +/-0.5 dB) on a radio
                We use an external receiver with audio feedback to AF1IN.
                The steps are: Signal generation (AM / 80%), Audio feedback investigation with (S+N)/N leveling

General Information:

Please always check this example script for unsuitable setting that may
destroy your DUT before connecting it to the instrument!
This example does not claim to be complete. All information has been
compiled with care. However errors can not be ruled out.

Please find more information about RsInstrument at
https://rsinstrument.readthedocs.io/en/latest/
"""

# --> Import necessary packets  
from RsInstrument import *
from time import sleep

resource = 'TCPIP0::10.205.0.30::inst0::INSTR'  # VISA resource string for the device
RsInstrument.assert_minimum_version('1.21.0')  # Ensure to use a dedicated minimum version of RsInstrument

# Define the device handle
# Instrument = RsInstrument(resource)
Instrument = RsInstrument(resource, reset=True, id_query=True, options="SelectVisa='rs'")
'''
- option SelectVisa:
    - 'SelectVisa = 'socket' - use no VISA implementation for socket connections - no need for a VISA-C installation
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
    Instrument.logger.log_to_console = False
    Instrument.logger.mode = LoggingMode.Off


def close():
    """Close the VISA session"""
    Instrument.close()


def comcheck():
    """Check communication with the device"""
    # Just knock on the door to see if instrument is present
    idn_response = Instrument.query_str('*IDN?')
    sleep(1)
    print('Hello, I am ' + idn_response)


def meas_setup(rf_freq, rf_start_level):
    """Switch CMA to Expert Mode and prepare  for first measurement with AM 80% / 1 kHz"""
    Instrument.write_str_with_opc("SYSTem:DISPlay:UPDate ON")  # Be sure the display is not switched off in remote mode
    Instrument.write('CONFigure:BASE:SCENario RXTest')  # Change to RX-Test scenario
    Instrument.write('SOURce:AFRF:GENerator1:RFSettings:CONNector RFCom')  # Route generator to RFCom
    Instrument.write_float('SOURce:AFRF:GENerator1:RFSettings:FREQuency ', rf_freq)  # Set generator frequency
    Instrument.write_float('SOURce:AFRF:GENerator1:RFSettings:LEVel ', rf_start_level)  # Define initial RF level
    Instrument.write('SOURce:AFRF:GENerator1:MSCHeme AM')  # Modulation = AM
    Instrument.write('SOURce:AFRF:GENerator1:MODulator:MDEPth 80')  # 80 % modulation depth
    Instrument.write('SOURce:AFRF:GEN:STATe ON')  # Turn output on
    Instrument.query_opc()  # CHeck for command completeness


def sn_proc(rf_level, goal, tolerance):
    """Perform leveling loop and end it as soon as (S+N)/N is inside the tolerance"""

    print('\nLeveling loop begins now ...')
    print('Start level is ', rf_level, 'dBm')
    x = 0
    while x < 20:
        # Read and then slice the amplitude list
        sn_read = Instrument.query_str('READ:AFRF:MEASurement1:MEValuation:SQUality:AIN1:AVERage?')
        sn_read = sn_read.split(",")  # Slice the amplitude list
        sn = float(sn_read[5])  # And use the 5th value of this list
        # Now compare SN to the desired level and change RF level according to the difference
        diff = goal - sn
        if abs(diff) < tolerance:
            print('\nTolerance level reached - Leveling loop is stopped now.')
            return sn, diff, rf_level  # Return the finally achieved values and end the loop
        rf_level = rf_level + diff
        print('New RF level is ', rf_level, " dBm")
        Instrument.write('SOURce:AFRF:GENerator1:RFSettings:LEVel ' + str(rf_level))
        x += 1
    raise Exception('WARNING! Leveling was not successful!')  # Throw an exception if loop is not successful


def final(level, snr, sn_goal, differ):
    """Display final level / ratio / difference to tolerance"""

    print(f'\nThe new RF level is {level:.2f} dBm')
    print(f'The (S+N)/N ratio is {snr:.2f} dB')
    print(f'The difference to the desired ratio ({sn_goal} dB) is {differ:.4f} dB \n\n')


#
# ---------------------------
# Main Program begins here
# only calling the functions
# ---------------------------
#
def main():
    # Predefine variables
    rf_freq = 120e6
    rf_start_level = -80
    sn_tol = 0.3  # Define the tolerance for (S+N)/N
    sn_goal = 20  # Define Goal (S+N)/N in dB
    comprep()
    comcheck()
    meas_setup(rf_freq, rf_start_level)
    snr, differ, level = sn_proc(rf_start_level, sn_goal, sn_tol)
    final(level, snr, sn_goal, differ)
    close()


main()
print("I'm done")
