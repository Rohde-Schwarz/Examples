"""
# GitHub examples repository path: Oscilloscopes/Python/RsInstrument

This Python example shows how to use FFT measurements with Zone trigger on a RTO6 oscilloscope.
Afterward, the peak measurements are transferred to the control PC and written in a CSV-file.

Preconditions:
- Installed RsInstrument Python module from pypi.org
- Installed VISA e.g. R&S Visa 7.2.x or newer

Tested with:
- RTO6, FW: v5.40.1.0
- Python 3.12+
- RsInstrument 1.82.1

Author: Christian Wicke (R&S)
Updated on 07.08.2024
Version: v1.0

RsInstrument documentation: https://rsinstrument.readthedocs.io/en/latest/

Technical support -> https://www.rohde-schwarz.com/support

Before running, please check this script for suitable settings and adjust the VISA Resource Name string!
"""

import csv

from RsInstrument import *  # The RsInstrument package is hosted on pypi.org, see Readme.txt for more details


def main():
    # Make sure you have the last version of the RsInstrument
    RsInstrument.assert_minimum_version('1.82')
    visa_resource_name = 'TCPIP::192.168.1.101::hislip0'
    file_path_pc = r'c:\temp\PeakList_Data.csv'
    fft_vars = {'f_start': '20E+6',
                'f_stop': '450E+6',
                'rbw': '300E+3'}
    peak_vars = {'p_threshold': '-65',
                 'p_count': '5'}
    zone1_points = [['95E+6', '-60'],
                    ['95E+6', '-50'],
                    ['105E+6', '-50'],
                    ['105E+6', '-60']]
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
    rto.write_with_opc('SYSTem:DISPlay:UPDate ON')
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

    # Display FFT
    rto.write_with_opc('CALCulate:MATH1:STATe ON')

    # Zone Trigger for FFT
    rto.write('MTESt:ADD \'Zone1\'')
    rto.write('MTESt:SOURce \'Zone1\',M1')
    rto.write('MTESt:CTYPe \'Zone1\',USER')
    rto.write('MTESt:SEGMent:ADD \'Zone1\'')

    for point in zone1_points:
        rto.write('MTESt:SEGMent:POINt:ADD \'Zone1\',0')
        rto.write('MTESt:SEGMent:POINt:X \'Zone1\',0,' + str(zone1_points.index(point)) + ',' + point[0])
        rto.write('MTESt:SEGMent:POINt:Y \'Zone1\',0,' + str(zone1_points.index(point)) + ',' + point[1])

    rto.write('MTESt:SEGMent:REGion \'Zone1\',0, INNER')
    rto.write_with_opc('MTESt:STATe \'Zone1\',ON')

    # Setup 'On-Violation' actions: NOACtion|SUCCess|VIOLation
    # Generates a beep sound.
    rto.write('MTESt:ONViolation:BEEP \'Zone1\',NOACtion')
    # Stops the waveform acquisition on mask violation.
    rto.write('MTESt:ONViolation:STOP \'Zone1\',VIOLation')
    # Saves a screenshot incl. the mask test results acc. to settings in "Menu">"Save/Recall">"Save"-tab>"Screenshot".
    # rto.write('MTESt:ONViolation:PRINt \'Zone1\',VIOLation')
    # Saves the waveform data to a file according to settings in "Menu">"Save/Recall">"Save"-tab>"Waveforms".
    # rto.write('MTESt:ONViolation:SAVewaveform \'Zone1\',VIOLation')
    # Creates and saves a report using the settings.
    # rto.write('MTESt:ONViolation:REPort \'Zone1\',VIOLation')
    # Sends a pulse to the [Trigger Out] connector on the rear panel.
    # rto.write('MTESt:ONViolation:TRIGgerout \'Zone1\',VIOLation')
    # Starts an external application. Tap "Config Executable" to set the application path and parameters.
    # rto.write('MTESt:ONViolation:RUNexec \'Zone1\',VIOLation')

    # Setup Trigger System
    rto.write('TRIGger1:EVENt:EVENt SEQuence')
    rto.write('TRIGger1:SEQuence:TYPE AZ')
    rto.write('TRIGger1:ZONE:EXPRession:DEFine \'Zone1\'')
    rto.query_opc()

    # Peak list setup
    rto.write('MEASurement1:SOURce M1')
    rto.write('MEASurement1:MAIN PLISt')
    rto.write('MEASurement1:SPECtrum:RESult12:MODE ABS')
    rto.write('MEASurement1:SPECtrum:ATHReshold ' + peak_vars['p_threshold'])
    rto.write('MEASurement1:SPECtrum:RESult1:COUNt ' + peak_vars['p_count'])

    with rto.visa_tout_suppressor() as sup:
        # Arming measurement
        rto.write_with_opc('SINGle')

    if sup.get_timeout_occurred():
        print(f'No zone violation occurred within {rto.opc_timeout} ms')
    else:
        print(f'Zone violation occurred. Writing CSV-file to {file_path_pc}')
        # Display Peak List for Measurement1
        rto.write_with_opc('MEASurement1:ENABle ON')

        # Query Peak List for Measurement1
        result_table = rto.query_bin_or_ascii_float_list('MEASUrement:RESult?')

        # Prepare 'result_table' for CSV export
        csv_list = [result_table[i:i + 2] for i in range(0, len(result_table), 2)]

        # Create CSV-file and write data
        fields = ['Frequency', 'Value']

        with open(file_path_pc, "w", newline='') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fields, quoting=csv.QUOTE_MINIMAL)

            # Writing CSV-file Header with 'Frequency (Hz)' and 'Value (dBm)'
            csv_writer.writeheader()
            # Writing each pair per row and converting the frequency value to SI format
            for freq, value in csv_list:
                csv_writer.writerow({'Frequency': value_to_si_string(freq, ".6g", 3), 'Value': value})

    # Close the session to the instrument
    rto.close()


if __name__ == "__main__":
    main()
