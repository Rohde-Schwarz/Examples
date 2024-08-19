"""
# GitHub examples repository path: Oscilloscopes/Python/RsInstrument

This Python example shows how to conduct an EMC pre-compliance measurement on a RTO6 oscilloscope.
Therefore, a trigger mask acc. CISPR Band-C specifications is set up conducting a +Peak measurement.
Afterward, a screenshot and the peak values violating the mask are transferred to the control PC and written to a CSV-file.

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

from RsInstrument import *  # The RsInstrument package is hosted on pypi.org, see Readme.txt for more details
import csv


def main():
    # Make sure you have the last version of the RsInstrument
    RsInstrument.assert_minimum_version('1.82')
    visa_resource_name = 'TCPIP::192.168.1.101::hislip0'
    # FFT variables for CISPR Band-C (30 MHz to 300 MHz) measurements
    fft_vars = {'f_start': '30E+6',
                'f_stop': '300E+6',
                'rbw': '120E+3'}
    mask_points = [['30E+6', '50'],
                   ['30E+6', '40'],
                   ['230E+6', '40'],
                   ['230E+6', '47'],
                   ['1E+9', '47'],
                   ['1E+9', '47.5'],
                   ['230E+6', '47.5'],
                   ['230E+6', '40.5'],
                   ['30E+6', '40.5'],
                   ['30E+6', '50.5']]
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
    rto.write('DISPlay:DIAGram:GRID ON')
    rto.query_opc()

    # Channel1 setup
    rto.write('CHAN1:SCAL 0.05')
    rto.write('TIM:SCAL 0.0001')
    rto.write('CHAN1:COUP DC')
    rto.write('CHAN1:WAV:TYPE SAMP')
    rto.write('LAY:SIGNal:UNASsign C1W1')

    # Acquisition settings
    rto.write('ACQ:POIN:AADJ ON')
    rto.write('ACQ:POIN:MAX 50E+6')
    rto.write('ACQ:POIN:AUTO RECL')

    # FFT settings for Channel1, trace mode '+Peak'
    rto.write("CALCulate:MATH1 'FFTmag(C1W1)'")
    rto.write('CALCulate:MATH1:FFT:STARt ' + fft_vars['f_start'])
    rto.write('CALCulate:MATH1:FFT:STOP ' + fft_vars['f_stop'])
    rto.write('CALCulate:MATH1:FFT:BANDwidth:RESolution:VALue ' + fft_vars['rbw'])
    rto.write('CALCulate:MATH1:FFT:LOGScale LOG')
    rto.write('CALC:MATH1:FFT:MAGN:SCAL DBUV')
    rto.write('CALC:MATH1:FFT:MAGN:RANG 100')
    rto.write('CALC:MATH1:FFT:MAGN:LEV 90')
    rto.write('CALC:MATH1:ARIT OFF')
    rto.write('CALC:MATH1:FFT:FRAM:ARIT MAXH')

    # Display FFT in LOG scale and 'Spectrum' color
    rto.write_with_opc('CALCulate:MATH1:STATe ON')
    rto.write_with_opc("DISP:COL:SIGN14:ASS 'Temperature'")
    rto.write_with_opc('DISP:COL:SIGN14:USE ON')
    
    # Zone Trigger for FFT
    rto.write('MTESt:ADD \'VAC_Radiated_QP_3M\'')
    rto.write('MTESt:SOURce \'VAC_Radiated_QP_3M\',M1')
    rto.write('MTESt:CTYPe \'VAC_Radiated_QP_3M\',USER')
    rto.write('MTESt:SEGMent:ADD \'VAC_Radiated_QP_3M\'')

    for point in mask_points:
        rto.write('MTESt:SEGMent:POINt:ADD \'VAC_Radiated_QP_3M\',0')
        rto.write('MTESt:SEGMent:POINt:X \'VAC_Radiated_QP_3M\',0,' + str(mask_points.index(point)) + ',' + point[0])
        rto.write('MTESt:SEGMent:POINt:Y \'VAC_Radiated_QP_3M\',0,' + str(mask_points.index(point)) + ',' + point[1])

    rto.write('MTESt:SEGMent:REGion \'VAC_Radiated_QP_3M\',0, INNER')
    rto.write_with_opc('MTESt:STATe \'VAC_Radiated_QP_3M\',ON')

    # Stops the waveform acquisition on mask violation.
    rto.write('MTESt:ONViolation:STOP \'VAC_Radiated_QP_3M\',VIOLation')

    # Setup Trigger System
    rto.write('TRIGger1:EVENt:EVENt SEQuence')
    rto.write('TRIGger1:SEQuence:TYPE AZ')
    rto.write('TRIGger1:ZONE:EXPRession:DEFine \'VAC_Radiated_QP_3M\'')
    rto.query_opc()

    with rto.visa_tout_suppressor() as sup:
        # Arming measurement
        rto.write_with_opc('SINGle')

    if sup.get_timeout_occurred():
        print(f'No zone violation occurred within {rto.opc_timeout} ms')
    else:
        # Query Peak List for Measurement1
        level_list = rto.query_bin_or_ascii_float_list('CALCulate:MATH1:DATA:VALues?')
        # Get screenshot
        file_path_instr = r'c:\Temp\Measurement_Screenshot.png'
        file_path_pc = r'c:\temp\Measurement_Screenshot.png'

        # Create screenshot and transfer to PC
        rto.write_str("HCOPy:DEVice1:LANGuage PNG")
        rto.write_str(f"MMEMory:NAME '{file_path_instr}'")
        rto.write_str_with_opc("HCOPy:IMMediate1")
        rto.read_file_from_instrument_to_pc(file_path_instr, file_path_pc)
        rto.write_with_opc(f"MMEMory:DELete '{file_path_instr}'")
        print(f'\nTransferred screenshot to {file_path_pc}')

        # Close the session to the instrument
        rto.close()

        step = (float(fft_vars['f_stop'])-float(fft_vars['f_start']))/len(level_list)
        i = float(fft_vars['f_start'])
        freq_lvl_list = []
        for v in level_list:
            freq_lvl_list.append(i)
            freq_lvl_list.append(v)
            i += step

        # Prepare 'result_table' for CSV export
        csv_list = [freq_lvl_list[i:i + 2] for i in range(0, len(freq_lvl_list), 2)]

        # Create CSV-file and write data
        file_path_csv = r'c:\temp\Measurement_Violations.csv'
        fields = ['Frequency', 'Value']

        with open(file_path_csv, "w", newline='') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fields, quoting=csv.QUOTE_MINIMAL)

            # Writing CSV-file Header with 'Frequency (Hz)' and 'Value (dBuV)'
            csv_writer.writeheader()
            # Writing each pair per row that violate the limits
            for freq, value in csv_list:
                if (float(freq) >= 30e+6 and float(value) >= 40) or (float(freq) >= 230e+6 and float(value) >= 40.5) or (float(freq) >= 1e+9 and float(value) >= 47):
                    csv_writer.writerow({'Frequency': freq, 'Value': value})
        print(f'\nSaved CSV file to {file_path_csv}')

    # Close the session to the instrument
    rto.close()


if __name__ == "__main__":
    main()
