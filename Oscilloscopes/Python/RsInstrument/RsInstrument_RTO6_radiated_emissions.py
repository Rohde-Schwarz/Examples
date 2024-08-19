"""
# GitHub examples repository path: Oscilloscopes/Python/RsInstrument

This Python example shows how to use FFT measurements on a RTO6 oscilloscope.
Afterward, a screenshot of the FFT measurement and spectrogram is transferred to the control PC.

Preconditions:
- Installed RsInstrument Python module from pypi.org
- Installed VISA e.g. R&S Visa 7.2.x or newer

Tested with:
- RTO6, FW: v5.40.1.0
- Python 3.12+
- RsInstrument 1.82.1

Author: Christian Wicke (R&S)
Updated on 05.08.2024
Version: v1.0

RsInstrument documentation: https://rsinstrument.readthedocs.io/en/latest/

Technical support -> https://www.rohde-schwarz.com/support

Before running, please check this script for suitable settings and adjust the VISA Resource Name string!
"""

from RsInstrument import *  # The RsInstrument package is hosted on pypi.org, see Readme.txt for more details
import time


def main():
    # Make sure you have the last version of the RsInstrument
    RsInstrument.assert_minimum_version('1.82')
    visa_resource_name = 'TCPIP::192.168.1.101::hislip0'
    # fft_vars.scaling_mode: auto|manual. In 'auto' the values 'maximum' and 'range' are ignored
    fft_vars = {'f_start': '20E+6',
                'f_stop': '450E+6',
                'rbw': '300E+3',
                'maximum': '-10',
                'range': '75',
                'scaling_mode': 'auto'}
    peak_vars = {'p_threshold': '-70',
                 'p_count': '10'}
    try:
        # Adjust the VISA Resource string to fit your instrument
        rto = RsInstrument(visa_resource_name, id_query=True, reset=True, options="SelectVisa='rs'")
        rto.logger.mode = LoggingMode.On
        rto.visa_timeout = 5000  # Timeout for VISA Read Operations
        rto.opc_timeout = 8000  # Timeout for opc-synchronised operations
        rto.instrument_status_checking = True  # Error check after each command
    except Exception as ex:
        print('Error initializing the instrument session:\n' + ex.args[0])
        exit()

    print(f'Device IDN: {rto.idn_string}')
    print(f'Device Options: {",".join(rto.instrument_options)}\n')

    # Reset to get a defined state
    rto.reset()
    rto.write('SYSTem:DISPlay:UPDate ON')
    rto.query_opc()

    # Channel1 setup
    rto.write('CHAN1:COUP DC')
    rto.write('LAY:SIGNal:UNASsign C1W1')

    # FFT settings for Channel1
    rto.write("CALCulate:MATH1 'FFTmag(C1W1)'")
    rto.write('CALCulate:MATH1:FFT:STARt ' + fft_vars['f_start'])
    rto.write('CALCulate:MATH1:FFT:STOP ' + fft_vars['f_stop'])
    rto.write('CALCulate:MATH1:FFT:BANDwidth:RESolution:VALue ' + fft_vars['rbw'])
    rto.write('CALCulate:MATH1:FFT:MAGNitude:SCALe DBM')

    # Only executed if fft_vars.scaling_mode is set to 'manual'
    # Sets vertical maximum and range
    if fft_vars['scaling_mode'] == 'manual':
        rto.write('CALCulate:MATH1:FFT:MAGNitude:RANGe ' + fft_vars['range'])
        rto.write('CALCulate:MATH1:FFT:MAGNitude:LEVel ' + fft_vars['maximum'])

    # Display FFT and Spectrogram
    rto.write_with_opc('CALCulate:MATH1:FFT:SPECtrogram:STATe ON')
    rto.write_with_opc('CALCulate:MATH1:STATe ON')

    # Peak list setup
    rto.write('MEASurement1:SOURce M1')
    rto.write('MEASurement1:MAIN PLISt')
    rto.write('MEASurement1:SPECtrum:RESult12:MODE ABS')
    rto.write('MEASurement1:SPECtrum:ATHReshold ' + peak_vars['p_threshold'])
    rto.write('MEASurement1:SPECtrum:RESult1:COUNt ' + peak_vars['p_count'])

    # Display Peak List for Measurement1
    rto.write('MEASurement1:ENABle ON')

    # Get screenshot
    file_path_instr = r'c:\Temp\Device_Screenshot.png'
    file_path_pc = r'c:\temp\Device_Screenshot.png'

    # Wait until Spectrogram has acquired enough waveforms
    while rto.query_int('ACQuire:AVAilable?') < 475:
        time.sleep(1.0)

    # Create screenshot and transfer to PC
    rto.write_str("HCOPy:DEVice1:LANGuage PNG")
    rto.write_str(f"MMEMory:NAME '{file_path_instr}'")
    rto.write_str_with_opc("HCOPy:IMMediate1")
    rto.read_file_from_instrument_to_pc(file_path_instr, file_path_pc)
    rto.write_with_opc(f"MMEMory:DELete '{file_path_instr}'")
    print(f'\nTransferred screenshot to {file_path_pc}')

    # Close the session to the instrument
    print(rto.query_all_errors_with_codes())
    rto.close()


if __name__ == "__main__":
    main()
