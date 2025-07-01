"""
# GitHub examples repository path: Oscilloscopes/Python/RsInstrument

$$$$$This Python example shows how to conduct power sequencing measurements up to 8-channels on the MXO oscilloscope to the controller PC.

Preconditions:
- Installed RsInstrument Python module from pypi.org
- Installed VISA e.g. R&S Visa 7.2.x or newer

Tested with:
- MXO, FW: v2.5.2.2
- Python 3.12+
- RsInstrument 1.100.0

Example calls:
Demo mode:
    python RsInstrument_MXO_8CH_power_sequencing.py --mode demo

Live mode with 8 channels:
    python RsInstrument_MXO_8CH_power_sequencing.py --mode live
    python RsInstrument_MXO_8CH_power_sequencing.py --mode live --channels 8

Live mode with 6 channels:
    python RsInstrument_MXO_8CH_power_sequencing.py --mode live --channels 6

Author: Christian Wicke (R&S)
Updated on 28.05.2025
Version: v1.0

Technical support -> https://www.rohde-schwarz.com/support

Before running, please check this script for suitable settings and adjust the VISA Resource Name string!
"""

from RsInstrument import *  # The RsInstrument package is hosted on pypi.org, see Readme.txt for more details
import os, sys, argparse

def ensure_ref_files_on_scope(mxo, ref_file_names, local_ref_dir='reference-files', scope_ref_dir='/home/instrument/userData/storage/deviceDemo/8power_seq/'):
    print('Checking for reference files on scope...')
    for ref_file in ref_file_names:
        scope_path = f"{scope_ref_dir}{ref_file}"
        # Ensure reference files are on the scope
        if not mxo.file_exists(scope_path):
            print(f"Copying {ref_file} to scope...")
            local_path = os.path.join(local_ref_dir, ref_file)
            mxo.send_file_from_pc_to_instrument(local_path, scope_path)

def demo_mode(mxo: RsInstrument):
    ref_file_names = [
        'c1_12V.ref', 'c2_5V.ref', 'c3_3p3.ref', 'c4_1p5.ref',
        'c6_1p0.ref', 'c5_1p1.ref', 'c7_0p5.ref', 'c8_fan_pwm.ref'
    ]
    scope_ref_dir = '/home/instrument/userData/storage/deviceDemo/8power_seq/'

    # Ensure reference files are on the scope
    ensure_ref_files_on_scope(mxo, ref_file_names, local_ref_dir='reference-files')

    # Display colors for the channels
    display_values = [
        4294967040,
        4278255360,
        4294926336,
        4285699839,
        4294692761,
        4287627189,
        4294945259,
        4291001599
    ]

    mxo.write(':CHANnel1:STATe 0')
    # Set the display colors for the channels
    for i in range(1, len(display_values) + 1):
        cmd = f':DISPlay:COLor:SIGNal:COLor R{i},{display_values[i-1]}'
        mxo.write(cmd)

    for idx, ref_file in enumerate(ref_file_names, start=1):
        mxo.write_with_opc(f":REFCurve{idx}:NAME '{scope_ref_dir}{ref_file}'")
        mxo.write(f":REFCurve{idx}:OPEN")
    mxo.write(':REFCurve1:RESTore')

    #List of tuples with scale and position values for the reference curves
    refcurves_values = [(2,-3),
                        (2,-1),
                        (2,0),
                        (2,-3),
                        (2,-1.5),
                        (2,-3),
                        (2,-1.5),
                        (2,-3)]

    for i in range(1, len(refcurves_values) + 1):
        scale, position = refcurves_values[i-1]
        cmd = f':REFCurve{i}:SCALe {scale}'
        mxo.write_with_opc(cmd)
        cmd = f':REFCurve{i}:POSition {position}'
        mxo.write_with_opc(cmd)

    configure_layout_and_nodes(mxo,'R')

    #List of tuples with scale and position values for the reference curves
    refcurves_values = [(2,-3),
                        (1,1),
                        (0.5,0),
                        (0.25,-3),
                        (0.2,1.2),
                        (0.2,-3),
                        (1,0),
                        (1,-3)]

    for i in range(1, len(refcurves_values) + 1):
        scale, position = refcurves_values[i-1]
        cmd = f':REFCurve{i}:SCALe {scale}'
        mxo.write_with_opc(cmd)
        cmd = f':REFCurve{i}:POSition {position}'
        mxo.write_with_opc(cmd)

    press_any_key_to_continue('All reference curves are set. Press any key to continue...')

    # Configure the delay measurements for the reference curves
    configure_measurements(mxo,'R')

def live_measurement(mxo: RsInstrument, num_channels=8):
    mxo.write('STOP')
    mxo.write('TIMebase:SCALe 50E-3')
    mxo.write('TIMebase:HORizontal:POSition 150e-3')
    for i in range(1, num_channels+1):
        # Adjust the channel scale for each channel (e.g. 2V/div)
        mxo.write(f'CHANnel{i}:SCALe 2')
        mxo.write(f'CHANnel{i}:STATe ON')

    mxo.write('TRIGger:MODE NORMal')
    mxo.write('TRIGger:MEVents:MODE SINGle')
    mxo.write('TRIGger:EVENt1:SOURce C1')
    mxo.write('TRIGger:EVENt1:TYPE EDGE')
    mxo.write('TRIGger:EVENt1:EDGE:SLOPe POSitive')
    # Adjust the trigger level to measurement setup (e.g. 3.5V)
    mxo.write('TRIGger:EVENt1:LEVel1:VALue 3.5')

    configure_layout_and_nodes(mxo, 'C', num_channels)

    # Wait for the trigger event to conduct measurements
    mxo.write('SINGle')
    press_any_key_to_continue('Once triggered, press any key to continue...')
    # Configure the delay measurements for the channels
    configure_measurements(mxo, 'C', num_channels)

def configure_layout_and_nodes(mxo, signal_prefix='R', num_channels=8):
    """Configures the layout and nodes on the oscilloscope for the specified channels. Sets the signal sources, layout parameters, and node types."""
    for i in range(2, num_channels + 1):
        mxo.write(f'LAYout:DIAGram{i}:ENABle 1')
        mxo.write(f'LAYout:DIAGram{i}:SOURce {signal_prefix}{i}')

    for i in range(1, num_channels):
        mxo.write(f'LAYout:NODE{i}:ENAB 1')

    node_children = {
        7: [('DIAGRAM', 7), ('DIAGRAM', 8)],
        6: [('DIAGRAM', 5), ('DIAGRAM', 6)],
        5: [('NODE', 6), ('NODE', 7)],
        4: [('DIAGRAM', 3), ('DIAGRAM', 4)],
        3: [('DIAGRAM', 1), ('DIAGRAM', 2)],
        2: [('NODE', 3), ('NODE', 4)],
        1: [('NODE', 2), ('NODE', 5)]
    }
    for node, children in node_children.items():
        for idx, (ctype, cid) in enumerate(children, start=1):
            mxo.write(f'LAYout:NODE{node}:CHILdren{idx}:CONTent:TYPE {ctype}')
            mxo.write(f'LAYout:NODE{node}:CHILdren{idx}:CONTent:ID {cid}')
        mxo.write(f'LAYout:NODE{node}:STYPe VERTICAL')

def configure_measurements(mxo, signal_prefix='R', num_channels=8):
    """Configures the measurements on the oscilloscope for the specified channels. Sets the signal sources, measurement types (e.g. DELay), reference levels, and layout parameters for the measurement display."""
    mxo.write(':DISPlay:DIAGram:GRID 0')
    mxo.write(':DISPlay:DIAGram:CROSshair 0')
    for i in range(1, num_channels):
        mxo.write(f'MEASurement{i}:SOURce {signal_prefix}{i}')
        mxo.write(f'MEASurement{i}:SSRC {signal_prefix}{i+1}')
    for i in range(1, num_channels):
        mxo.write(f'MEASurement{i}:MAIN DELay')
    mxo.write('LAYout:NODE1:STYPe HORIZONTAL')
    mxo.write('LAYout:NODE1:RATio 0.83')
    for i, middle in enumerate([65, 90], start=1):
        mxo.write(f'REFLevel{i}:RELative:MODE USER')
        mxo.write(f'REFLevel{i}:RELative:MIDDle {middle}')
    measurements = [(4, 2, 2), (5, 1, 2)]
    for meas, ref, level in measurements:
        mxo.write(f'MEASurement{meas}:REFLevel{ref}:REFerence {level}')

def initialize_instrument(visa_name):
    """Initializes the instrument and returns the device object."""
    try:
        mxo = RsInstrument(visa_name, id_query=True, reset=True, options="SelectVisa='rs'")
        mxo.logger.mode = LoggingMode.On
        mxo.visa_timeout = 5000
        mxo.opc_timeout = 8000
        mxo.instrument_status_checking = True
        print(f'Device IDN: {mxo.idn_string}')
        print(f'Device Options: {",".join(mxo.instrument_options)}\n')
        mxo.write('SYSTem:PRESet')
        mxo.write('SYSTem:DISPlay:UPDate ON')
        return mxo
    except Exception as ex:
        print(f'Error initializing the instrument session:\n{ex.args[0]}')
        sys.exit()

def get_screenshot(mxo, instr_dir='/home/instrument/userData', filename='Print.png', pc_path=r'c:\temp\MXO58_8powerSeq_screenshot.png'):
    """Creates a screenshot on the device, transfers it to the PC, and deletes the file on the device."""
    instr_file = f"{instr_dir}/{filename}"
    # Set the working directory on the device
    mxo.write_with_opc(f"MMEMory:CDIRectory '{instr_dir}'")
    # Set the file format for the screenshot
    mxo.write_with_opc("HCOPy:DEVice:LANGuage PNG")
    # Define the file name for the screenshot
    mxo.write_with_opc(f"MMEMory:NAME '{instr_file}'")
    # Create the screenshot
    mxo.write_with_opc('SYSTem:DISPlay:UPDate 1')
    mxo.write_with_opc("HCOPy:IMMediate")
    # Transfer the screenshot to the PC
    mxo.read_file_from_instrument_to_pc(instr_file, pc_path)
    # Clean up on the device
    mxo.write_with_opc(f"MMEMory:DELete '{instr_file}'")
    print(f'\nTransferring screenshot to {pc_path}')

def print_measurement_results(mxo, signal_prefix='R', num_channels=8):
    """Reads the measurement results for MEASurement1-7:RESult:ACTual? and prints them."""
    for i in range(1, num_channels):
        value = mxo.query(f"MEASurement{i}:RESult:ACTual?")
        print(f"Measurement {signal_prefix}{i}{signal_prefix}{i+1} Delay: {value}")

def main():
    parser = argparse.ArgumentParser(description='8-channel power sequencing example.')
    parser.add_argument('--mode', choices=['demo', 'live'], default='demo',
                        help="Select 'demo' for demo mode or 'live' for live measurement. Defaults to 'demo'.")
    parser.add_argument('--channels', '-c', type=int, default=8,
                        help="(only for live) Number of channels (1-8), default: 8")

    args = parser.parse_args()
    selected_mode = args.mode
    num_channels = args.channels if selected_mode == 'live' else 8

    mode_to_function = {
        'demo': demo_mode,
        'live': live_measurement
    }
    signal_prefix = 'R' if selected_mode == 'demo' else 'C'

    print(f'Starting "8-channel power sequencing" example: {selected_mode}')

    RsInstrument.assert_minimum_version('1.55.0')
    visa_name = 'TCPIP::10.102.100.21::hislip0'
    mxo = initialize_instrument(visa_name)

    if selected_mode == 'live':
        if not (1 <= num_channels <= 8):
            print("Error: Channel count must be between 1 and 8.")
            sys.exit(1)
        print(f"Live measurement with {num_channels} channels.")
        mode_to_function[selected_mode](mxo, num_channels)
    elif selected_mode == 'demo':
        print("Demo mode is starting.")
        mode_to_function[selected_mode](mxo)
    else:
        print("Invalid mode selected. Use '--mode demo' or '--mode live'.")
        sys.exit(1)

    get_screenshot(mxo)
    print_measurement_results(mxo, signal_prefix, num_channels)

    # Query for errors and close the session to the instrument
    print(mxo.query_all_errors_with_codes())
    mxo.close()

def press_any_key_to_continue(msg='Press any key to continue...'):
    input(msg)

if __name__ == "__main__":
    main()