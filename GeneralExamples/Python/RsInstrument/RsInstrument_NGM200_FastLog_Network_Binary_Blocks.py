"""

Created 2021/03

Author:                     Jahns_P
Version Number:             1
Date of last change:        2021/03/01
Requires:                   R&S NGM20x Power Supply,  FW 03.034 or newer and adequate options
                            Installed VISA e.g. R&S Visa 5.12.x or newer

Description:    Example of Data Logging with the NGM via network using the fast log function.
                


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
# from RsInstrument.RsInstrument import RsInstrument
# from RsInstrument.RsInstrument import BinFloatFormat, BinIntFormat

from time import sleep

# Define variables
resource = 'TCPIP0::10.205.0.41::inst0::INSTR'  # VISA resource string for the device

# Define the device handle, force selection of R&S VISA if available. If not, fall back to default VISA
RsInstrument.assert_minimum_version('1.17.0.72')
Instrument = RsInstrument(resource, True, True, "SelectVisa='rs'")
"""
Initializes new RsInstrument session. \n
For cleaner code, use the RsInstrument.from_existing_session(existing_session_obj)
Parameter options tokens examples:
- 'Simulate = True' - starts the session in simulation mode. Default: False
- 'SelectVisa = 'socket' - uses no VISA implementation for socket connections - you do not need any VISA-C installation
- 'SelectVisa = 'rs' - forces usage of Rohde&Schwarz Visa
- 'SelectVisa = 'ni' - forces usage of National Instruments Visa
- 'QueryInstrumentStatus = False' - same as driver.utilities.instrument_status_checking = False. Default: True.
:param resource_name: VISA resource name, e.g. 'TCPIP::192.168.2.1::INSTR'
:param id_query: if True: the instrument's model name is verified against the models supported by the driver and eventually throws an exception
:param reset: Resets the instrument (sends *RST) command and clears its status syb-system
:param options: string tokens alternating the driver settings
:param direct_session: Another driver object or pyVisa object to reuse the session instead of opening a new session
"""

# Define all the subroutines


def comprep():
    """Preparation of the communication (termination, etc...)"""
    # this kind of format ensures to get the information shown in the docstrings
    try:
        print(f'VISA Manufacturer: {Instrument.visa_manufacturer}')  # Confirm VISA package to be chosen
        Instrument.visa_timeout = 3000  # Timeout for VISA Read Operations
        Instrument.opc_timeout = 3000  # Timeout for opc-synchronised operations
        Instrument.instrument_status_checking = True  # Error check after each command
        Instrument.opc_query_after_write = True  # *OPC? query after each write command
        Instrument.clear_status()  # Clear status register
    except Exception as ex:
        print('Error initializing the instrument session:\n' + ex.args[0])
        exit()

    print(f'Device IDN: {Instrument.idn_string}')
    print(f'Device Options: {",".join(Instrument.instrument_options)}')


def measprep():
    """Preparation of the measurement process"""
    Instrument.write_str('INST OUT1')  # Choose channel 1 for the following commands
    Instrument.write_str('VOLT 12')  # Set U to 12V
    Instrument.write_str('CURR 1')  # Set I to 1A
    Instrument.write_str('OUTP:SEL 1')  # Activate the selected channel
    Instrument.write_str('OUTP:GEN 1')  # Activate Main Output

    Instrument.write_str('FLOG:SRATe S100')  # Set logging speed (sample rate)
    # The following parameters are available to set the log sample rate:
    # S100 / S001k / S010k / S050k / S250k  / S500K
    Instrument.write_str('FLOG:TARGet SCPI')  # Redirect fast log data to SCPI port (Remote Control)


def measure():
    """Initiate measurement, wait for the end of the process and read out the value"""
    Instrument.write_str('FLOG:STATe 1')  # Activate logging

    # --> Read the log data in the normal way (no conversion)
    sleep(1)  # Collect data for 1 s
    result = Instrument.query_bin_block('FLOG:DATA?')  # Initiate logging and read out binary block data into a string
    print(len(result))  # Give information about the number of read bytes (should be double value of sample rate here)
    print('Measurement result is ', result)  # Print binary block data (begins with "b'\x")

    # --> Read the log data and convert it into human readable values
    sleep(1)  # Collect data for one second
    Instrument.bin_float_numbers_format = BinFloatFormat.Single_4bytes  # Define binary format for conversion (4 Bytes means 32 bits)
    result2 = Instrument.query_bin_or_ascii_float_list('FLOG:DATA?')  # Read the binary block and convert it
    print(result2)  # Print the list

    # --> Directly transfer log data into a .bin file
    sleep(1)  # Wait for another second to collect data
    Instrument.query_bin_block_to_file(  # Again readout binary block, but now directly write into a .bin file
        'FLOG:DATA?',  # SCPI command is the same like before
        r'c:\test\bindata.bin',  # Specify filename and take care concerning format (\ could initiate a control character)
        append=False)  # Avoid appending in the file

    Instrument.write_str('FLOG:STATe 0')  # Deactivate logging


def close():
    """Close the VISA session"""
    Instrument.close()


# --------------------------
# Main program begins here
# --------------------------


comprep()
measprep()
measure()
close()

print("Program successfully ended.")
