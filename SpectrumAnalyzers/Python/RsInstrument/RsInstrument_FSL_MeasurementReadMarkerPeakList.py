'''

Created on 2022/01

Author: Jahns_P
Version Number: 1
Date of last change: 2022/01/18
Requires: FSL series SPA, FW 2.50 or newer and adequate options
- Installed RsInstrument Python module 1.19.0 or newer
- Installed VISA e.g. R&S Visa 5.12.x or newer

Description: Setup measurement, set Marker and request Marker Peak List


General Information:

Please always check this example script for unsuitable setting that may
destroy your DUT before connecting it to the instrument!
This example does not claim to be complete. All information has been
compiled with care. However errors can not be ruled out. 

Please find more information about RsInstrument at 
https://rsinstrument.readthedocs.io/en/latest/
'''

# --> Import necessary packets
from RsInstrument.RsInstrument import RsInstrument
from time import sleep

# Define variables
ressource='TCPIP0::10.205.0.155::INSTR'    # VISA resource string for the device
x=0  # For counters
loopResponse="1" # Variable for diverse loop requests
Response="0" # Variable for diverse requests
recdur = 10 # Time in seconds to find maxhold peaks

# Define the device handle
RsInstrument.assert_minimum_version("1.19") # Check for RsInstrument version and stop if version is less than 1.19
Instrument = RsInstrument(ressource, True, True, "SelectVisa='rs'")
'''
(ressource, True, True, "SelectVisa='rs'") has the following meaning:
(VISA-resource, id_query, reset, options)
- id_query: if True: the instrument's model name is verified against the models 
supported by the driver and eventually throws an exception.   
- reset: Resets the instrument (sends *RST) command and clears its status syb-system
- option SelectVisa:
			- 'SelectVisa = 'socket' - uses no VISA implementation for socket connections - you do not need any VISA-C installation
			- 'SelectVisa = 'rs' - forces usage of Rohde&Schwarz Visa
			- 'SelectVisa = 'ni' - forces usage of National Instruments Visa     
'''
##
## Define subroutines
##

def comprep():
    """Preparation of the communication (termination, timeout, etc...)"""
    
    print (f'VISA Manufacturer: {Instrument.visa_manufacturer}') # Confirm VISA package to be choosen
    Instrument.visa_timeout = 5000 # Timeout in ms for VISA Read Operations
    Instrument.opc_timeout = 3000 # Timeout in ms for opc-synchronised operations
    Instrument.instrument_status_checking = True # Error check after each command
    Instrument.clear_status() # Clear status register
  
    
def close():
    """Close the VISA session"""
    
    Instrument.close()


def comcheck():
    """Check communication with the device by requesting it's ID"""
    
    # Just knock on the door to see if instrument is present
    idnResponse = Instrument.query_str('*IDN?')
    sleep (1)
    print ('Hello, I am ' + idnResponse + '\n')
    
   
def measprep():
    """Prepare instrument for desired measurements
    In this case
    - Set Center Frequency to 1 GHz
    - Set Span to 1 GHz
    - Set Trace to Max Hold (and Positive Peak automatically)
    """

    Instrument.write_str('SYSTem:DISPlay:UPDate ON')  # Allow Display while instrument is under remote control
    Instrument.write_str('DISPlay:TRACe:Y:RLEVel 0 dBm')
    Instrument.write_str('FREQuency:CENTer 1e9') # Center Frequency to 2450 MHz
    Instrument.write_str('FREQuency:SPAN 1e9') # SPAN is 100 MHz now
    Instrument.write_str('DISPlay:TRACe1:MODE MAXHold') # Trace to Max Hold
    Instrument.write_str_with_opc('INITiate:CONTinuous OFF') # Stop continuous acquisition
    Instrument.write_str('SWEep:COUNt 20') # Perform 200 Single counts to collect Max Hold Values
    Instrument.write_str('INITiate:IMMediate') # Initiate single n single sweeps
    #sleep(5) # And wait some time for the collection to be completed

def peaklist():
    """Initialize continuous measurement, stop it after 10 seconds and query trace data"""

    Instrument.write_str('CALC:MARK:TRAC 1') # Start Marker 1 (at Trace 1)
    Instrument.write_str('CALC:MARK:FUNC:FPE:SORT X') # Marker sort mode to increasing frequency values
    Instrument.write_str('CALC:MARK:FUNC:FPE 3') # Define number of peaks to search
    resultnr = Instrument.query_str('CALC:MARK:FUNC:FPE:COUN?') # Request for number of peaks being found
    print('Number of selected Peaks = ', resultnr , '\n')
    resulty = Instrument.query_str('CALC:MARK:FUNC:FPE:Y?') # Request levels of found maxima
    print('Peak values in dBm: ', resulty)
    resultx = Instrument.query_str('CALC:MARK:FUNC:FPE:X?') # Requests frequency information of the found maxima
    print('Peak list frequency in Hz: ', resultx, '\n\n')

##
##-------------------------
## Main Program begins here 
##-------------------------
##
    
comprep()
comcheck()
measprep()
peaklist()
close()


print ("Programm succesfully ended.")