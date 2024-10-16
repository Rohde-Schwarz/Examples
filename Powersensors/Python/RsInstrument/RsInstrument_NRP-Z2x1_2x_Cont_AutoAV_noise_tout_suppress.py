"""
# GitHub examples repository path: not known yet

This Python example shows how to perform Continuous average measurements with NRP-Z2x1 power sensors.
The script will show all the steps from the general setup on.

Preconditions:
- Installed RsInstrument Python module from pypi.org
- Installed VISA e.g. R&S Visa 5.12.x or newer

Tested with:
- NRP-Z211, FW v.04.17, NRP-Z22, FW v.04.16
- Python 3.12
- RsInstrument 1.82.1

Author: R&S Product Management AE 1GP3 / PJ
Updated on 15.10.2024
Version: v1.0

Technical support -> https://www.rohde-schwarz.com/support

Before running, please always check your setup!
This example does not claim to be complete. All information have been
compiled with care. However, errors can’t be ruled out.

"""

# --> Import necessary packets and check for an adequate version of RsInstrument
from RsInstrument import *
from math import log10
from time import sleep


RsInstrument.assert_minimum_version('1.90')

# Define variables
#resource = 'RSNRP::0x00a6::101479::INSTR'  # VISA resource string for the device NRP-Z211
resource = 'RSNRP::0x0013::900001::INSTR'  # VISA resource string for the device NRP-Z22

freq = 1e9  # Working frequency
aperture = 250e-3  # Aperture time
smoothing = "OFF"  # Smoothing can be "ON" or "OFF", makes only sense for modulated signals.
takes = 100   # Number of measurements to take in complete for the analysis
wait_time = 0.2  # Wait time between single measurements. Has been set to 0.2 s originally.
nsr_ratio = 0.3  # Defines the intended maximal noise deviation in dB.
# If the ratio is too low, the sensor will return an error concerning "MTIME". A low nsr ratio also will lead to
# a higher number of exceptions. So if a lot of errors got caught, enlarge the value.
m_time = 30  # Defines the upper limit for the settling time (in s) of the auto average filter and so it limits
# the average filter length.


# Define the device handle
try:
    nrp = RsInstrument(resource, False, True, options="SelectVisa='rs', ")
except ResourceError as e:
    print(e.args[0])
    print('Your instrument is probably OFF...')
    # Exit now, no point of continuing
    exit(1)


# Define all the subroutines


def com_prep():
    """Preparation of the communication (termination, etc...)"""
    print(f'\nVISA Manufacturer: {nrp.visa_manufacturer}\n')  # Confirm VISA package to be chosen.
    nrp.instrument_status_checking = True  # Error check after each command, can be True or False.
    nrp.clear_status()  # Clear status register
    nrp.logger.log_to_console = False  # Route SCPI logging feature to console on (True) or off (False).
    nrp.logger.mode = LoggingMode.Off  # Switch On or Off SCPI logging.


def com_check():
    """Test the device connection, request ID as well as installed options"""
    print('Hello, I am ' + nrp.query('*IDN?'))
    print(f'\n Extended sensor information: \n {nrp.query('SYST:INFO?')}\n')


def meas_setup():
    """Prepare the sensor for the desired measurement task and perform zeroing"""
    nrp.write('SENS:FUNC "POW:AVG"')  # Sensor "Mode" is Average now.
    nrp.write(f'SENS:FREQ {freq}')
    nrp.write(f'SENS:POW:AVG:APER {aperture}')  # Define aperture time for the measurement.
    # It is always better to work with higher aperture time and a smaller average filter as this will save time.
    # For details take a look into your sensor's specifications sheet (section "Measurement time").
    # As an example the measurement time for continuous average is defined by
    # 2 × (aperture + 145 μs) × 2^N + 1.6 ms (2^N is the length of the average filter which only can be 2 to the
    # power of n (max. 65536)).
    nrp.write(f'SENS:POW:AVG:SMO:STAT {smoothing}')  # Would only improve the measurement for modulated signals.
    sleep(0.2)
    nrp.write('SENS:AVER:STAT ON')  # Averaging is on.
    nrp.write('SENS:AVER:COUN:AUTO ON')  # Averaging is set to auto filter mode.
    nrp.write(f'SENSe:AVERage:TCONtrol REPeat')  # Only provide values after the averaging filter content is complete.
    # The other way would be to set it to MOVing, which would already provide a measurement value also if the
    # number of filter elements is not reached at that moment.
    nrp.write(f'SENSe:AVERage:COUN:AUTO:TYPE NSR')  # Calculate AV Filter based on a noise component which is
    # defined as the magnitude of the level variation in dB caused by the inherent noise of the sensor (two standard
    # deviations).
    nrp.write(f'SENSe:AVERage:COUN:AUTO:MTIMe {m_time}')  # Sets an upper limit for the settling time (in s) of the
    # auto-averaging filter in the NSRatio mode and thus limits the length of the filter.
    nrp.write(f'SENSe:AVERage:COUN:AUTO:NSRatio {nsr_ratio}')  # Defines the intended maximal noise deviation in dB
    nrp.write('TRIG:SOUR IMM')  # Do not wait for a trigger event.

    # Perform sensor zeroing now.
    std_tmo = nrp.visa_timeout  # Read out standard timeout setting to reset it after the following procedure.
    nrp.visa_timeout = 10500  # Set the timeout variable to a time (in ms) that allows waiting for a successful zeroing.
    print('Please switch off test signal and confirm.')
    input()
    print('Start zeroing ...')
    nrp.write('CALibration:ZERO:AUTO ONCE')
    print('...Sensor is zeroed now.')
    nrp.visa_timeout = std_tmo
    print('Please enable test signal and confirm.')
    input()


def meas():
    nrp.write('INITiate:CONTinuous ON')  # Initiate a measurement (also resets Average filter content).
    m_list = []  # We collect all the measurement values in this list for evaluation after the gathering process.
    print('Begin measurement row now')
    for x in range(takes):
        value = "0,0"
        while value == "0,0":
            with nrp.visa_tout_suppressor(10000) as supp:  # Timeout suppressor defines timeout
                # (which will be set back to original value after usage).
                nrp.write('TRIGger:IMMediate')  # Initiate a trigger
                sleep(wait_time)
                value = nrp.query('FETCH?')  # Get the measurement values
            if supp.get_timeout_occurred():
                print('\n VisaTimeout occurred')

            if float(value.split(',')[0]) > 1:  # Too much noise can cause the result to be NAN (not a number),
                # which will be returned by a value of 9.91 E 37 (defined in the standard "1999 SCPI Syntax &
                # Style") . I such a case the measurement has to be repeated.
                value = "0,0"

        value = 10 * log10 (1000* float(value.split(',')[0]))  # Convert the desired measurement value to dBm (Z)
        print(f'\r Measurement {x}: {value:.4f} dBm, '
              f'AV Filter is set to {nrp.query('SENSe:AVERage:COUNt?')}',
              end='', flush=True)
        m_list.append(value)
        nrp.clear_status()
    print(f'\n Gathered {len(m_list)} valid values. The minimum value is {min(m_list):.3f} dBm '
          f'and the maximum value is {max(m_list):.4f} dBm.\n'
          f' This leads to a deviation range of \n -->{max(m_list)-min(m_list):.4f} dB\n using the following parameters:'
          f'\n- Aperture time of {aperture} s'
          f'\n- Smoothing is {smoothing}'
          f'\n- Noise deviation was set to {nsr_ratio} dB and used to recalculate '
          f'the average filter for each measurement.')


def close():
    """Close the VISA session"""
    nrp.close()


#  Main program begins here

com_prep()
com_check()
meas_setup()
meas()
close()

print("Program successfully ended.")
