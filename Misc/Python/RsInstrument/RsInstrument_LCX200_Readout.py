"""
# GitHub examples repository path: Misc/Python/RsInstrument

Created on 2022/07

Author: Jahns_P
Version Number: 1
Date of last change: 2022/07/25
Requires: LCXx00 with adequate options, FW 02.007 or newer

Description: Example about how to read out measurement data for capacitance measurements with internal BIAS

General Information:
Please always check this example script for unsuitable setting that may
destroy your DUT before connecting it to the instrument!
This example does not claim to be complete. All information has been
compiled with care. However, errors can not be ruled out.
"""

# --> Import necessary packets
import time

from RsInstrument import *

RsInstrument.assert_minimum_version("1.50")  # Check for RsInstrument version and stop if version number is too low

lcx = RsInstrument('TCPIP::10.205.0.151::hislip0', reset=True, id_query=True,
                   options="SelectVisa='rs' , LoggingMode = Off, LoggingToConsole = False")


def meas_prep():
    """Prepare LCX for desired measurement procedure"""
    lcx.write_str('FREQuency:CW 1e3')  # Set measurement frequency in Hz (Range is HW dependent)
    lcx.write_str('VOLTage:LEVel 1')  # Set test signal level in V !RMS! (Range: 0.01 - 10 V)
    # lcx.write_str('CURRent:LEVel 0.1')  # Set test signal current level (instead of voltage, Range: 0.0001 - 0.2 A)
    lcx.write_str('APERture LONG')  # Set the measurement time interval
    # Valid aperture / time interval values are:
    # SHORt (measurement time is >= 0.15 s)
    # MEDium (0.1 s)
    # LONG (0.5 s)
    # DEFault (sets measurement time to "SHORt")
    lcx.write_str('BIAS:CURRent:LEVel 0.1')  # Set internal bias current level to 0.1 A (Range: 0 - 0.2 A)
    lcx.write_str('BIAS:VOLTage:LEVel 1')  # Set internal BIAS voltage level to 1 V (Range: 0 - 10 V
    lcx.write_str('BIAS:STATe ON')  # Activate Bias Voltage


def measure():
    """Initiate measurement, read the measurands and check for accuracy of Z and PHI"""
    lcx.write_str('FUNCtion:MEASurement:TYPE C')  # Define the measurement type
    # Valid values: C(apacitor), L(for inductivity), R(esistor), T(ransformer)
    lcx.write_str('FUNCtion:IMPedance:TYPE CSRS')  # Measurement function is Cs - Rs to get the ESR
    # Serial or parallel measurement is calculated - the principle of the bridge is not changed by hardware
    # Valid values are CPD | CPQ | CPG | CPRP | CSD | CSQ | CSRS
    # LPD | LPQ | LPG | LPRP | LSD | LSQ | LSRS
    # RX | RPB | RDC | MTD | NTD | ZTD | ZTR | GB | YTD | YTR
    # For details please refer to the manual chapter 11.10 (FUNCtion subsystem)
    lcx.write_str('FUNCtion:IMPedance:RANGe:AUTO 0')  # Change impedance range to auto off
    lcx.query_opc()  # Test for command completion
    lcx.write_str('MEASure:MODE TRIGgered')  # Set single triggered measurement mode (continuous off)
    # It is always recommended to switch off the continuous mode during remote control
    x = 0
    while x < 10:  # Loop for dedicated number of measurements
        lcx.write_str_with_opc('INITiate:IMMediate')  # Start a new measurement and check for command completion (OPC)
        time.sleep(.05)  # Short pause before measurement values are available
        print('\nTry ', x+1)
        print('The current measurement values are (Cs in F, Rs in Ohm) ', lcx.query_str('FETCh?'), '.')
        print('The corresponding values for Z (in Ohm) and PHI (in degrees) are ',
              lcx.query_str('FETCh:IMPedance?'), '.')
        print('And measurement accuracy of Z (%) and PHI (°) is ', lcx.query_str('MEASure:ACCuracy?'), '.')
        print('Current Range is ', lcx.query_str('FUNCtion:IMPedance:RANGe:VALue?'), '.')

        x += 1


def close():
    """Switch off all active generators or BIAS and close connection"""
    lcx.write_str('BIAS:STATe OFF')  # Switch Bias Voltage off
    lcx.close()


def main():
    meas_prep()
    measure()
    close()


main()
print("\nI'm done")
