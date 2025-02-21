"""
# GitHub examples repository path: not known yet

This Python example shows how to perform a time related measurement using the R&S NRPxxP / NRPxxS(N)power sensors.
In some cases it is necessary to only gather the power of a part of the signal (for example the payload). When
talking about Wi-Fi, this can be achieved at least using Burst Average as well as Time Slot measdurements.

In the first step, the script will show how the SMBV100B is prepared to provide a Wi-Fi IEEE 802.11ax signal. If no
generator with the capability to produce a Wi-Fi signal is available, one could also work with an adequate pulse
modulated setup (for example PRI of 210 ms, idle time of 100 µs). The generator only will be controlled if the variable
"gen_pres" in the variable section at the first lines of the script is set to 1. Please change it to any other value
if using a different setup.

The power sensor part of the script explains different ways to perform the measurement:
- using Burst average measurements
- working with time slots


Preconditions:
- Installed RsInstrument Python module from pypi.org
- Installed VISA e.g. R&S Visa 5.12.x or newer
- Adequate options for the instruments (for example SMBV100B with K54/ K142/ K520 / KB106)

Tested with:
- SMBV100B, FW 5.30.047.32
- NRP18P, FW 01.40.24102201
- NRP18SN, FW 03.20.24090501
- Python 3.12
- RsInstrument 1.90.0

Author: R&S Product Management AE 1GP3 / PJ
Updated on 21.02.2025
Version: v1.0

Technical support -> https://www.rohde-schwarz.com/support

Before running, please always check your setup!
This example does not claim to be complete. All information have been
compiled with care. However, errors can’t be ruled out.
"""

# --> Import necessary packets
from RsInstrument import *

# Define variables
# Devices
gen_pres = 1
generator = 'TCPIP::SMBV100B-104078.local::hislip0'  # VISA resource string for the rf generator
#sensor = 'USB::0x0AAD::0x0143::100328::INSTR'  # VISA resource string for NRP18P
sensor = 'USB::0x0AAD::0x0139::102246::INSTR'  # VISA resource string for NRP18SN

# Signal definition in general
freq = 5e9  # RF frequency for the measurement in Hz
pwr = -10  # RF power level
pre_len = 20e-6  # length of preamble

# Measurement in general
measurements = 5  # Number of readings to take
trg_lev = -20  # Trigger level for the signal (will be calculated from the power provided by the source)
av_count = 128  # Size of the averaging filter

# Burst Average variables
do_tol = 1e-6  # Dropout tolerance for the burst (To prevent power drops being erroneously interpreted as pulse end)
dropout = 90e-6  # Trigger dropout time in s
end_cut = 1e-6

# Time Slot variables
tg_period = 165e-6

# Define the device handle
if gen_pres == 1:
    smbv = RsInstrument(generator, False, True, options="SelectVisa='rs'")
nrp = RsInstrument(sensor, False, True, options="SelectVisa='rs'")



# Define all the subroutines

def gen_prep():
    """Generator preparation (communication, connection and options, perform Wi-Fi setup"""
    print(f'\nVISA Manufacturer: {smbv.visa_manufacturer}\n')  # Confirm VISA package to be chosen
    smbv.visa_timeout = 5000  # Timeout for VISA Read Operations
    smbv.opc_timeout = 5000  # Timeout for opc-synchronised operations
    smbv.instrument_status_checking = True  # Error check after each command, can be True or False
    smbv.clear_status()  # Clear status register
    smbv.logger.log_to_console = False  # Route SCPI logging feature to console on (True) or off (False)
    smbv.logger.mode = LoggingMode.Off  # Switch On or Off SCPI logging
    # Now test the device connection, request ID as well as installed options
    print('Hello, I am ' + smbv.query('*IDN?'), end=" ")
    print('and I have the following options available: \n' + smbv.query('*OPT?'))
    # Perform Wi-Fi setup and enable the signal
    smbv.write('*RST')
    smbv.query_opc()
    smbv.write('SOURce1:BB:WLNN:FBLock1:STANdard WAX')  # Set signal to IEEE 802.11ax
    smbv.write('SOURce1:BB:WLNN:STATe 1')  # Enable Wi-Fi
    smbv.write(f'SOURce1:FREQuency:CW {freq}')
    smbv.write(f'SOURce1:POWer:LEVel:IMMediate:AMPLitude {pwr}')
    smbv.query_opc()
    smbv.write('OUTPut1:STATe 1')
    smbv.query_opc()
    print(f'\nGenerator is prepared and provides a signal now (Frequency: {freq/1e9} GHz, Power Level: {pwr} dBm)...')

def sens_prep():
    """Power Sensor preparation (communication, connection and options"""
    print(f'\nVISA Manufacturer: {nrp.visa_manufacturer}\n')  # Confirm VISA package to be chosen
    nrp.visa_timeout = 3000  # Timeout for VISA Read Operations
    nrp.opc_timeout = 3000  # Timeout for opc-synchronised operations
    nrp.instrument_status_checking = True  # Error check after each command, can be True or False
    nrp.clear_status()  # Clear status register
    nrp.logger.log_to_console = False  # Route SCPI logging feature to console on (True) or off (False)
    nrp.logger.mode = LoggingMode.Off  # Switch On or Off SCPI logging
    # --> Now test the device connection, request ID as well as installed options
    nrp.write('*RST')
    nrp.query_opc()
    print('Hello, I am ' + nrp.query('*IDN?'), end=" ")
    print('and I have the following options available: \n' + nrp.query('*OPT?'))
    # --> Perform Wi-Fi setup and enable the signal



def burst_prep():
    """Preparation of the burst average measurement. The timeslot mode is used to measure the average power of a
    definable number of successive timeslots within a frame structure with equal spacing. The measurement result is
    an array with the same number of elements as timeslots. Each element represents the average power in a particular
    timeslot."""
    nrp.write(f'SENSe:FREQuency {freq}')
    nrp.write('SENSe:FUNCtion "POWer:BURSt:AVG"')  # Change to burst average measurement
    # In burst average mode, only internal trigger events from the signal are evaluated, irrespective of the setting
    # of the TRIGger:SOURce parameter. The TRIGger:DELay parameter is also ignored, so that the measurement interval
    # begins exactly when the signal exceeds the trigger level.
    nrp.write('TRIGger:LEVel:UNIT dBm')  # Set the trigger level unit to dBm (unit is W after preset)
    nrp.write(f'TRIGger:LEVel {trg_lev}')
    nrp.query_opc()  # Check for command completeness
    nrp.write('UNIT:POWer dBm')  # Power now will be displayed in dBm (is W after preset)
    # Next line is only for using the NRPxxP series:
    #nrp.write('SENS:BWID:VID "FULL"')  # Enable full video bandwidth for highest precision (same like after preset)
    nrp.write(f'SENSe:TIMing:EXCLude:STARt {pre_len}')  # Exclude the preamble at the beginning of the measurement
    nrp.write(f'SENSe:TIMing:EXCLude:STOP {end_cut}')  # Exclude unwanted effects at the end of the burst
    nrp.write(f'SENSe:POWer:BURSt:DTOLerance {do_tol}')  # Just for sake of completeness: Sets the dropout tolerance,
    # a time interval in which the pulse end is only recognized if the signal level no longer exceeds the trigger level.
    nrp.write('SENSe:AVERage:COUNt:AUTO OFF')  # Averaging mode to "manual" (Is "ON" after preset)
    nrp.write('SENSe:AVERage:STATe ON')  # Is alreday "ON" after preset, setting count to on is same like "OFF"
    nrp.write(f'SENSe:AVERage:COUNt {av_count}')  # Define averaging filter size, range: 1 to 1048576, preset: 1024
    nrp.query_opc()
    nrp.write('INITiate:CONTinuous ON')  # Switch on Continuous measurement (is "OFF" after preset)
    nrp.query_opc()
    print('\nThe power sensor is set up for the Burst Average mode...')

def burst_meas():
    print('The measurement now begins...\n')
    x = 1
    while x in range (measurements+1):
        print(f'Measurement {x}: {nrp.query_float('FETch?'):.4f} dBm')  # Request and print measurement result
        x += 1
    nrp.write('INITiate:CONTinuous OFF')  # Switch off continuous measurement
    nrp.write('ABORt')  # Immediately interrupts the current measurement.


def t_slot_prep():
    """Preparation of the time slot average measurement. The timeslot mode is used to measure the average power of a
    successive timeslot."""
    nrp.write(f'SENSe:FREQuency {freq}')
    # In timeslot mode, internal and external trigger events from the signal are evaluated depending on the settings
    # of the TRIGger:SOURce parameter. It is essential to define the TRIGger:DELay parameter to ensure that the
    # beginning of the first slot to be measured coincides with the delayed trigger point.
    nrp.write('SENSe:FUNCtion "POWer:TSLot:AVG"')  # Change to time slot measurement
    nrp.write('TRIGger:SLOPe POS')  # Positive trigger slope (rising signal)
    nrp.write('TRIGger:LEVel:UNIT dBm')  # Set the trigger level unit to dBm (unit is W after preset)
    nrp.write(f'TRIGger:LEVel {trg_lev}')
    nrp.write('TRIGger:SOURce INT')  # Set trigger to RF (is "INT" already after preset)
    nrp.write('TRIGger:DELay 0')
    nrp.write(f'TRIGger:DTIMe {dropout}')  # Sets the dropout time for the internal trigger source. During this time,
    # the signal power must exceed (negative trigger slope) or undercut (positive trigger slope) the level defined by
    # the trigger level and trigger hysteresis. At least, this time must elapse before triggering can occur again.
    nrp.query_opc()
    nrp.write('UNIT:POWer dBm')  # Power now will be displayed in dBm (is W after preset)
    nrp.write(f'SENSe:TIMing:EXCLude:STARt {pre_len}')  # Set the length of the preamble to exclude it
    nrp.write(f'SENSe:TIMing:EXCLude:STOP {end_cut}')  # Set the length of the preamble to exclude it
    nrp.write('SENSe:AVERage:STATe ON')  # Averaging mode to "manual" (Is "ON" after preset)
    nrp.write('SENSe:AVERage:COUNt:AUTO OFF')  # Averaging mode to "manual" (Is "ON" after preset)
    nrp.write(f'SENSe:AVERage:COUNt {av_count}')  # Define averaging filter size, range: 1 to 1048576, preset: 1024
    nrp.write('SENSe:POWer:TSLot:AVG:COUNt 1')  # Sets the number of simultaneously measured timeslots.
    nrp.write(f'SENSe:POWer:TSLot:AVG:WIDTh {tg_period}') # Timeslot width (covering all the period time!)
    nrp.query_opc()
    print('\nThe power sensor is set up for the Timeslot Average mode...')

def t_slot_meas():
    print('The measurement now begins...\n')
    x = 1
    while x in range (measurements+1):
        nrp.write('INITiate:IMMediate')
        nrp.query_opc()
        print(f'Measurement {x}: {nrp.query_float('FETch?'):.4f} dBm')
        x += 1


def close():
    """Close the VISA session"""
    if gen_pres == 1 :
        smbv.write("OUTPut1:STATe 0")
        print('\nGenerator output is switched off.')
        smbv.close()
    nrp.close()


#  Main program begins here

if gen_pres == 1:
    gen_prep()
burst_prep()
burst_meas()
t_slot_prep()
t_slot_meas()
close()
print("Program successfully ended.")