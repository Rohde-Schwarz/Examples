"""
# GitHub examples repository path: Powersensors/Python/RsInstrument/

This Python example shows how to set up the NRT2 and perform a standard measurement.

Preconditions:
- Installed RsInstrument Python module from pypi.org
- Installed VISA e.g. R&S Visa 5.12.x or newer

Tested with:
- NRT2, FW: v02.10
- Python 3.10
- RsInstrument 1.54.0

Author: R&S Customer Support / PJ
Updated on 13.11.2023
Version: v2.0

Technical support -> https://www.rohde-schwarz.com/support

Before running, please always check your setup!
This example does not claim to be complete. All information have been
compiled with care. However, errors can’t be ruled out.

"""

# --> Import necessary packets  
from RsInstrument import *
RsInstrument.assert_minimum_version('1.54')  # Ensure to use a dedicated minimum version of RsInstrument

# Define variables
resource = 'TCPIP0::x.x.x.x::inst0::INSTR'  # VISA Resource String of the device
nrt = RsInstrument(resource, id_query=True, reset=True)  # Define the device handle


def close():
    """Close the VISA session"""
    nrt.close()


def comcheck():
    """Check the communication to the instrument"""
    # Just knock on the door to see if instrument is present
    idn_response = nrt.query('*IDN?')
    print('Hello, I am ' + idn_response)


def prep_meas():
    """Prepare the instrument for the desired measurement (sensor 1)"""
    nrt.write("SENS1:FREQ 1 GHz")  # Define measurement frequency is 1GHz now
    nrt.write("CALC1:CHAN1:FEED1 'POW:FORW:AVER,POW:REV'")  # Chose measurement functions to FWD & REV power
    # Available measurements:
    # POWer:FORWard:AVERage, POWer:FORWard:CCDFunction, POWer:FORWard:PEP, POWer:ABSorption:AVERage, POWer:CFACtor
    # POWer:ABSorption:PEP, POWer:FORWard:AVERage:BURSt, POWer:ABSorption:AVERage:BURSt, POWer:OFF, POWer:REVerse
    # POWer:SWRatio, POWer:RLOSs, POWer:RCOefficient, POWer:RFRatio,
    #
    nrt.write("UNIT1:POWER DBM")  # Set power unit to dBm
    # Available units:
    # dBm, dBμV, W
    #
    nrt.query_opc()  # Check for command completeness


def meas():
    """Perform measurement on first sensor and print the acquired values"""
    nrt.write("TRIGGER:IMM")  # Initiate trigger event and wait for completion through errorcheck
    print('The current measurement response for CH1 is :', nrt.query("SENS1:DATA?"))


# Main Program begins here

comcheck()
prep_meas()
meas()
close()

print("I'm done")
