"""
# GitHub examples repository path: Oscilloscopes/Python/RsInstrument

This Python example shows how to use measurements on the MXO oscilloscope to the controller PC.
The MXO arbitrary generator is used as a source signal. Please connect the 'Gen 1' output to the 'C1' input.

Preconditions:
- Installed RsInstrument Python module from pypi.org
- Installed VISA e.g. R&S Visa 5.12.x or newer

Tested with:
- MXO, FW: v1.4.2.2
- Python 3.9+
- RsInstrument 1.54.0

Author: R&S Miloslav Macko
Updated on 11.09.2023
Version: v1.0

Technical support -> https://www.rohde-schwarz.com/support

Before running, please always check this script for unsuitable setting !
This example does not claim to be complete. All information have been
compiled with care. However, errors can’t be ruled out.
"""

from RsInstrument import *  # The RsInstrument package is hosted on pypi.org, see Readme.txt for more details
from packaging import version


def main():
    # Make sure you have the last version of the RsInstrument
    RsInstrument.assert_minimum_version('1.54.0')
    # mxo = None
    try:
        # Adjust the VISA Resource string to fit your instrument
        mxo = RsInstrument('TCPIP::10.112.0.37::hislip0', id_query=True, reset=True, options="SelectVisa='rs'")
        fw_version = version.parse(mxo.instrument_firmware_version)
        if fw_version < version.parse("1.4"):
            raise Exception(f"Your instrument has an older FW Version ({fw_version}) not supported by this example. "
                            f"The minimum supported version is 1.4.2.2. Please make a FW update")
        mxo.logger.mode = LoggingMode.On
        mxo.visa_timeout = 5000  # Timeout for VISA Read Operations
        mxo.opc_timeout = 8000  # Timeout for opc-synchronised operations
        mxo.instrument_status_checking = True  # Error check after each command
    except Exception as ex:
        print('Error initializing the instrument session:\n' + ex.args[0])
        exit()

    print(f'Device IDN: {mxo.idn_string}')
    print(f'Device Options: {",".join(mxo.instrument_options)}\n')

    # Reset to get a defined state
    mxo.write('*RST')
    mxo.write('SYSTem:DISPlay:UPDate ON')
    # Horizontal and Vertical settings
    mxo.write('CHANnel1:STATe ON')
    mxo.write('CHANnel1:RANGe 2.0')
    mxo.write('CHANnel1:COUPling DCLimit')
    mxo.write('TIMebase:SCALe 5E-5')
    # Trigger settings
    mxo.write('TRIGger:MODE AUTO')
    mxo.write('TRIGger:EVENt1:SOURce C1')
    mxo.write('TRIGger:EVENt1:LEVel1:VALue 0.5')
    mxo.write('TRIGger:EVENt1:TYPE EDGE')
    mxo.write('TRIGger:EVENt1:EDGE:SLOPe POSitive')
    # Arb gen settings
    mxo.write('WGENerator1:ENABle OFF')
    mxo.write('WGENerator1:FUNCtion:SELect SINusoid')
    mxo.write('WGENerator1:FREQuency 10KHZ')
    mxo.write('WGENerator1:VOLTage:VPP 1.000')
    mxo.write_with_opc('WGENerator1:ENABle ON')
    # Measurements settings
    mxo.write('MEASurement1:SOURce C1')
    mxo.write('MEASurement1:MAIN FREQuency')
    mxo.write('MEASurement1:ENABle ON')

    mxo.write('MEASurement2:SOURce C1')
    mxo.write('MEASurement2:MAIN RMS')
    mxo.write('MEASurement2:ENABle ON')

    mxo.write('MEASurement3:SOURce C1')
    mxo.write('MEASurement3:MAIN PDEL')
    mxo.write('MEASurement3:ENABle ON')
    mxo.query_opc()
    # Start the acquisition, wait for it to finish
    mxo.write_with_opc('SINGle')

    # Read the measurements.
    # Query with OPC makes sure, that if the result is not available,
    # you get an error immediately without having to wait for the VISA timeout.
    freq = mxo.query_float_with_opc('MEASurement1:RESult:ACTual?')
    amp_rms = mxo.query_float_with_opc('MEASurement2:RESult:ACTual?')
    amp_pp = mxo.query_float_with_opc('MEASurement3:RESult:ACTual?')

    print("\nMeasurement results:")
    print(f"Frequency: {freq:0.3f} Hz")
    print(f"Amplitude RMS: {amp_rms:0.3f} V")
    print(f"Amplitude Peak-to-peak: {amp_pp:0.3f} V")

    print("\nMeasurement results statistics:")
    # For statistics measurement, we set the number of acquisitions to 100
    mxo.write('ACQuire:COUNt 100')
    mxo.write('MEASurement1:STATistics:ENABle ON')
    mxo.write_with_opc('SINGle')  # Perform 100 acquisitions and then stop

    freq_max = mxo.query_float_with_opc('MEASurement1:RESult:PPEak?')
    freq_min = mxo.query_float_with_opc('MEASurement1:RESult:NPEak?')
    freq_mean = mxo.query_float_with_opc('MEASurement1:RESult:AVG?')
    freq_rms = mxo.query_float_with_opc('MEASurement1:RESult:RMS?')
    freq_sdev = mxo.query_float_with_opc('MEASurement1:RESult:STDDev?')
    print(f"Frequency: "
          f"max {freq_max:0.5f} Hz, "
          f"min {freq_min:0.5f} Hz, "
          f"mean {freq_mean:0.5f} Hz,"
          f"rms {freq_rms:0.5f} Hz, "
          f"s-dev {freq_sdev:0.5f} Hz")

    amp_rms_max = mxo.query_float_with_opc('MEASurement2:RESult:PPEak?')
    amp_rms_min = mxo.query_float_with_opc('MEASurement2:RESult:NPEak?')
    amp_rms_mean = mxo.query_float_with_opc('MEASurement2:RESult:AVG?')
    amp_rms_rms = mxo.query_float_with_opc('MEASurement2:RESult:RMS?')
    amp_rms_sdev = mxo.query_float_with_opc('MEASurement2:RESult:STDDev?')

    print(f"Amplitude RMS: "
          f"max {amp_rms_max:0.5f} V, "
          f"min {amp_rms_min:0.5f} V, "
          f"mean {amp_rms_mean:0.5f} V,"
          f"rms {amp_rms_rms:0.5f} V, "
          f"s-dev {amp_rms_sdev:0.5f} V")

    amp_pp_max = mxo.query_float_with_opc('MEASurement3:RESult:PPEak?')
    amp_pp_min = mxo.query_float_with_opc('MEASurement3:RESult:NPEak?')
    amp_pp_mean = mxo.query_float_with_opc('MEASurement3:RESult:AVG?')
    amp_pp_rms = mxo.query_float_with_opc('MEASurement3:RESult:RMS?')
    amp_pp_sdev = mxo.query_float_with_opc('MEASurement3:RESult:STDDev?')

    print(f"Amplitude Peak-Peak: "
          f"max {amp_pp_max:0.5f} V, "
          f"min {amp_pp_min:0.5f} V, "
          f"mean {amp_pp_mean:0.5f} V,"
          f"rms {amp_pp_rms:0.5f} V, "
          f"s-dev {amp_pp_sdev:0.5f} V")

    mxo.close()


if __name__ == "__main__":
    main()
