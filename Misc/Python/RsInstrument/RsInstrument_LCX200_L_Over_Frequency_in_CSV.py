# -*- coding: utf-8 -*-
"""
# GitHub examples repository path: Misc/Python/RsInstrument

Created on 2024/02

Author: Customer Support / PJ
Version Number: 1
Date of last change: 2024/02/06
Requires: LCXx00 with adequate options, FW 02.043 or newer

Description:
Example about how to test a DUT's frequency response, write it into a CSV file  and get a graphical view of the results

General Information:
Please always check this example script for unsuitable setting that may
destroy your DUT before connecting it to the instrument!
This example does not claim to be complete. All information has been
compiled with care. However, errors can not be ruled out.
"""

# --> Import necessary packets
from RsInstrument import *

# --> Predefine variables
start_freq = 500e3  # Start frequency in Hz
stop_freq = 10e6  # Stop frequency in Hz (Range is HW dependent)
freq_step = 50e3  # Frequency scan step in Hz
meas_interv = 'MED'  # Set the measurement time interval. Valid values are: SHORt (0.15 s), MEDium (0.1 s), LONG (0.5 s)
compensate = 'N'  # Choose if Open / Short Compensation and Reset will be performed (possible values: Y and N).
file_path_name = 'C:\\tempdata\\fresponse.csv'

RsInstrument.assert_minimum_version("1.60")  # Check for RsInstrument version and stop if version number is too low

lcx = RsInstrument('TCPIP::10.205.0.67::hislip0', reset=False, id_query=True,
                   options="SelectVisa='rs' , LoggingMode = Off, LoggingToConsole = False")


def meas_prep():
    """Prepare LCX for desired measurement procedure: perform full compensation and set diverse parameters"""
    print('\n')
    print('Hello, you are connected to: ', lcx.query('*IDN?'))
    print('The following options are installed on the instrument: ', lcx.query('*OPT?'))
    print('\n')

    # --> Measurement setup
    if compensate == "Y":
        lcx.reset()
    lcx.write(f'FREQuency:CW {start_freq}')  # Set measurement start frequency as predefined
    lcx.write(f'APERture {meas_interv}')  # Change the measurement time interval according to the preset value

    # --> If defined, perform full Open and Short Calibration
    if compensate == "Y":
        lcx.opc_timeout = 180000
        _cont = input("Please prepare clamps for OPEN calibration, click on the Python Console and press Enter")
        print('The following procedure now can take up to 3 minutes...')
        lcx.write_with_opc('CORRection:OPEN:EXECute')
        lcx.write('CORRection:OPEN:STATe 1')
        print('OPEN compensation is done and activated\n')
        lcx.write('DISPlay:WINDow:DIALog:CLEar:ALL')
        _cont = input("Please prepare clamps for SHORT calibration, click on the Python Console and press Enter")
        lcx.write_with_opc('CORRection:SHORt:EXECute')
        print('The following procedure now can take up to 3 minutes...')
        lcx.write('CORRection:SHORT:STATe 1')
        print('SHORT compensation is done and activated\n')
        lcx.write('DISPlay:WINDow:DIALog:CLEar:ALL')
        lcx.opc_timeout = 30000


def measure():
    """Initiate measurement, read the measurements and check for accuracy of Z and PHI"""
    _cont = input("Please connect your DUT now, click on the Python Console and press Enter")

    lcx.write('FUNCtion:IMPedance:RANGe:AUTO 1')  # Be sure to have the impedance range set to AUTO

    csv_out = open(file_path_name, 'w')  # Open CSV file for writing
    csv_out.write('f in Hz;Z in Ohm;PHI in °;Vm in mV;L in H;C in F;Accuracy in %;PHI-acc. in °\n')  # Write header data
    # The script will log
    # - Frequency f in Hz
    # - Impedance Z in Ohm
    # - Phase Angle PHI in °
    # - Measurement voltage Vm in mV
    # - Inductance L in H
    # - Capacitance C in F
    # - Frequency accuracy in %
    # - PHI accuracy in °

    freq = start_freq
    while freq <= stop_freq:  # Loop for dedicated number of measurements
        # 1. Set frequency and change to triggered measurement mode
        lcx.write(f'FREQuency:CW {freq}')
        lcx.query_opc()
        lcx.write('MEASure:MODE TRIGgered')  # It is not recommended to perform measurements in continuous mode

        # 2. Perform measurement
        print(f'Performing measurement on {freq:0.4} Hz')
        csv_out.write(f'{freq:0.4};')

        lcx.write('*TRG')  # Start a new measurement and fetch values
        phi_z = lcx.query_bin_or_ascii_float_list('FETCh:IMPedance?')  # Get Phi and Z
        csv_out.write(f'{phi_z[0]:0.3};{phi_z[1]:0.2};')
        print(f'Z = {phi_z[0]:0.3} OHM, PHI ={phi_z[1]:0.2} °')

        lcx.write('MEASure:MODE CONTinuous')  # Reading of the measurement voltage only works in continuous mode
        readback_voltage = lcx.query_float('MEASure:VOLTage?')  # Get Vm (measurement voltage)
        csv_out.write(f'{readback_voltage:0.3};')
        print(f'Vm = {readback_voltage:0.3} V')
        lcx.write('MEASure:MODE TRIGgered')

        lcx.write('FUNCtion:MEASurement:TYPE L')  # Set measurement type according to the front panel key L (Inductance)
        lcx.write('FUNCtion:IMPedance:TYPE LSRS')  # Measurement function is LSRS (L serial / R serial) now
        # Serial or parallel measurement is calculated - the principle of the bridge is not changed by hardware
        # Valid values are CPD | CPQ | CPG | CPRP | CSD | CSQ | CSRS
        # LPD | LPQ | LPG | LPRP | LSD | LSQ | LSRS
        # RX | RPB | RDC | MTD | NTD | ZTD | ZTR | GB | YTD | YTR
        # For details please refer to the manual chapter 11.10 (FUNCtion subsystem)
        lcx.write('*TRG')
        ls_rs = lcx.query_bin_or_ascii_float_list('FETCH?')  # Get C and R
        csv_out.write(f'{ls_rs[0]:0.3};')  # Only log L
        print(f'L = {ls_rs[0]:0.3} H')  # Only log L

        lcx.write('FUNCtion:MEASurement:TYPE C')  # Set measurement type according to the front panel key C(apacity)
        lcx.write('FUNCtion:IMPedance:TYPE CSRS')  # Measurement function is Cs - Rs to get the ESR
        lcx.write('*TRG')
        cs_rs = lcx.query_bin_or_ascii_float_list('FETCH?')  # Get C and R
        csv_out.write(f'{cs_rs[0]:0.3};')  # Only log C
        print(f'C = {cs_rs[0]:0.3} F')  # Only log C

        accz_accphi = lcx.query_bin_or_ascii_float_list('MEASure:ACCuracy?')
        csv_out.write(f'{accz_accphi[0]:0.2};{accz_accphi[1]:0.2}\n')  # Only log C
        print(f'Acc Z = {accz_accphi[0]:0.2} %, Acc PHI = {accz_accphi[1]:0.2} °\n')  # Only log C

        freq = freq + freq_step


def close():
    """Switch off all active generators or BIAS and close connection"""
    lcx.write('BIAS:STATe OFF')  # Switch Bias Voltage off
    lcx.close()


def main():
    meas_prep()
    measure()
    close()


main()
print("\nI'm done")
