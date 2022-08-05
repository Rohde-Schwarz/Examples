"""
# GitHub examples repository path: VectorNetworkAnalyzers/Python/RsInstrument

Created 2022/08

Author:                     Jahns_P
Version Number:             1
Date of last change:        2022/08/02
Requires:                   R&S ZNL, FW 1.42 or newer and adequate options
                            Installed VISA e.g. R&S Visa 5.12.x or newer

Description:    Example to measure S21 attenuation and write the results into a CSV file.


General Information:

Please always check this example script for unsuitable setting that may
destroy your DUT before connecting it to the instrument!
This example does not claim to be complete. All information has been
compiled with care. However, errors can not be ruled out.
"""

# --> Import necessary packets  
from RsInstrument import *
from time import sleep

# Define variables
resource = 'TCPIP0::10.205.0.73::INSTR'  # ZNL VISA resource string for the device
PcFile = r'c:\tempdata\logfile.CSV'  # Name and path of the logfile
points = 401  # Number of sweep points

# Prepare instrument communication

RsInstrument.assert_minimum_version("1.50")  # Check for RsInstrument version and stop if version number is too low
znl = RsInstrument(resource, reset=True, id_query=False,
                   options="SelectVisa='rs' , LoggingMode = Off, LoggingToConsole = False")


def comprep():
    """Preparation of the communication (termination, etc...)"""
    print(f'VISA Manufacturer: {znl.visa_manufacturer}')  # Confirm VISA package to be chosen
    znl.visa_timeout = 5000  # Timeout for VISA Read Operations
    znl.opc_timeout = 5000  # Timeout for opc-synchronised operations
    znl.clear_status()  # Clear status register
    znl.write_str('SYSTem:DISPlay:UPDate ON')  # Keep display on while under remote control


def close():
    """Close the VISA session"""
    znl.close()


def comcheck():
    """Check communication with the device"""
    # Just knock on the door to see if instrument is present
    idnresponse = znl.query_str('*IDN?')
    sleep(1)
    print('Hello, I am ' + idnresponse)
    print('And I am equipped with the following options: ', znl.instrument_options)


def meassetup():
    """Assign additional settings to the channel"""
    #
    # Setup for CH1
    #
    znl.write_str('SENSe1:FREQuency:STARt 0.01GHZ')  # Start frequency to 10 MHz
    znl.write_str('SENSe1:FREQuency:STOP 1.0GHZ')  # Stop frequency to 1 GHz

    znl.write('SENSe1:SWEep:POINts '+str(points))  # Set number of sweep points to the defined number
    znl.write_str('CALCulate1:PARameter:MEASure "Trc1", "S21"')  # Measurement now is S21
    sleep(0.5)  # It will take some time to perform a complete sweep - wait for it
    znl.write_str('DISPlay:WINDow1:TRACe1:Y:SCALe:AUTO ONCE')  # Enable auto scaling for trace 1
    znl.write_str_with_opc("INIT1:CONT OFF")  # Set single sweep mode and stop acquisition


def filewrite():
    """Read trace data and write it into a local file"""
    logfile = open(PcFile, "w")  # Open logfile
    logfile.write("Frequ / Hz; Atten. / db")   # Write table headline
    logfile.write("\n")
    xpoints = znl.query_int('SENSe1:SWEep:POINts?')  # Request number of frequency points
    print(f'The current trace contains {points} frequency points')
    tracedata = znl.query_str('CALCulate1:DATA? FDAT')  # Get measurement values for complete trace
    tracelist = list(map(str, tracedata.split(',')))  # Convert the received string into a list
    freqdata = znl.query_str('CALCulate1:DATA:STIMulus?')  # Get frequency list for complete trace
    freqlist = list(map(str, freqdata.split(',')))  # Convert the received string into a list
    ''' 
    Important information:
    
    Alternatively the following commands will also work:
    TRACe:DATA:Response? CH1Data to get linear magnitude values instead of dB
    TRACe:DATA:STIMulus? CH1Data to get the frequency values in Hz
        
    If you want to compare the stimulus frequency data with markers on the screen,
    keep in mind to set the corresponding marker to "discrete" (Menu: Mkr - Marker Props),
    otherwise you will get interpolated frequency steps shown on the display. 
    '''

    # Now write frequency and magnitude for each point and close the file if done
    x = 0
    while x < xpoints:
        logfile.write(freqlist[x] + ";")
        logfile.write(tracelist[x] + "\n")
        x = x + 1

    logfile.close()


def main():
    comprep()
    comcheck()
    meassetup()
    filewrite()
    close()


main()
print()
print("I'm done. Data is written to ", PcFile)
