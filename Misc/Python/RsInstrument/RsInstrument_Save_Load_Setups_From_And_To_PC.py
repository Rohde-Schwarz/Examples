"""

Created 2021/11

Author:                     Winfried Jansen
Version Number:             1
Date of last change:        2021/11/15
Requires:                   R&S ZNB, FW 3.12 or newer and adequate options
                            Installed VISA e.g. R&S Visa 5.12.x or newer

Description:    Example how to:
- save the current instrument status as a setup file (see path instrument_file)
- transfer the created setup to the PC (see path pc_file)
- reset the instrument
- delete the setup on the instrument
- transfer the setup from the PC to the instrument
- Apply the setup
- The result is the same state of the instrument as at the beginning of the example



General Information:

Please always check this example script for unsuitable setting that may
destroy your DUT before connecting it to the instrument!
This example does not claim to be complete. All information has been
compiled with care. However errors can not be ruled out. 
"""

# --> Import necessary packets  
from RsInstrument import *
from time import sleep

# Define fixed values
# VISA resource string for the device
resource = 'TCPIP0::10.112.0.225::HISLIP'
# PC File Path
pc_file = r'c:\temp\setup_on_pc.znx'
instrument_file = r'c:\Users\Public\Documents\Rohde-Schwarz\VNA\RecallSets\setup_on_instr.znx'

# Define the device handle
# Instrument = RsInstrument(resource)
Instrument = RsInstrument(resource, True, False, "SelectVisa='rs'")
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

    print(f'VISA Manufacturer: {Instrument.visa_manufacturer}')     # Confirm VISA package to be choosen
    Instrument.visa_timeout = 5000                                  # Timeout for VISA Read Operations
    Instrument.opc_timeout = 5000                                   # Timeout for opc-synchronised operations
    Instrument.instrument_status_checking = True                    # Error check after each command, can be True or False
    Instrument.clear_status()
    
    
                                       # Clear status register


def close():
    """Close the VISA session"""

    Instrument.close()


def comcheck():
    """Check communication with the device"""

    # Just knock on the door to see if instrument is present
    idnResponse = Instrument.query_str('*IDN?')
    sleep(1)
    print('Hello, I am ' + idnResponse)


# Main Program begins here
comprep()
comcheck()
print("We store the current setup as file on the ZNx, and transfer it to the control PC")
input("Press Enter to continue...\n")

# Store the setup in the instrument
Instrument.write_str_with_opc(f'MMEM:STOR:STAT 1,"{instrument_file}"')
# Transfer the file to the control PC

Instrument.read_file_from_instrument_to_pc(instrument_file, pc_file)
print("Now we delete the setup file on the ZNx and reset the instrument")
input("Press Enter to continue...\n")
Instrument.write_str_with_opc(f'MMEM:DEL "{instrument_file}"')
Instrument.reset()

print("The next step transfers the file from the control PC back to the instrument and applies it")
input("Press Enter to continue...\n")
# Transfer the file to the instrument
Instrument.send_file_from_pc_to_instrument(pc_file, instrument_file)
# Load the transferred setup
Instrument.write_str_with_opc(f'MMEM:LOAD:STAT 1,"{instrument_file}"')
close()

print("Now you should see the same state of the instrument as before you started this example")