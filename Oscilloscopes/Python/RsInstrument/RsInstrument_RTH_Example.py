"""
# GitHub examples repository path: Oscilloscopes/Python/RsInstrument

This Python example shows how to transfer waveform data (ASCII and binary format)
+ screenshot from RTH oscilloscope to the controller PC. The RTH probe compensation
signal can be used for a simple test.

Preconditions:
# - Installed RsInstrument Python module from pypi.org
- Installed VISA e.g. R&S Visa 5.12.x or newer

Tested with:
- RTH1002, FW: v1.80.3.4
- Python 3.8.5
- PyVISA 1.11.0
- RsInstrument 1.6.0.32

Author: R&S Customer Support
Updated on 29.09.2020
Version: v1.2

Technical support -> https://www.rohde-schwarz.com/support

Before running, please always check this script for unsuitable setting !
This example does not claim to be complete. All information have been
compiled with care. However, errors can’t be ruled out.

"""

from RsInstrument import *  # The RsInstrument package is hosted on pypi.org, see Readme.txt for more details
import matplotlib.pyplot as plt
from time import time


def main():
    # Make sure you have the last version of the RsInstrument
    RsInstrument.assert_minimum_version('1.22.0')
    rth = None
    try:
        # adjust the VISA Resource string to fit your instrument
        rth = RsInstrument('TCPIP::192.168.0.1::INSTR', True, False)
        # rth = RsInstrument('USB0::0x0AAD::0x012F::1317.5000K02/103176::INSTR', True, False)
        rth.visa_timeout = 6000  # Timeout for VISA Read Operations
        rth.opc_timeout = 3000  # Timeout for opc-synchronised operations
        rth.instrument_status_checking = True  # Error check after each command
    except Exception as ex:
        print('Error initializing the instrument session:\n' + ex.args[0])
        exit()
    
    print(f'Device IDN: {rth.idn_string}')
    print(f'Device Options: {",".join(rth.instrument_options)}\n')

    rth.clear_status()
    rth.reset()

    # basic settings - to test with RTH probe compensation signal
    rth.write_str("TIM:SCAL 0.001")
    rth.write_str("ACQ:WAV FULL")  # relevant if time scale is ≥50 ms/div
    rth.write_str("CHAN1:SCAL 0.02")
    rth.write_str("CHAN1:POS -2.5")
    rth.write_str("TRIG:LEV1:VAL 0.05")

    rth.write_str("TRIG:MODE SING")
    start = time()
    rth.write_str_with_opc("RUN")
    stop = time()
    print('RTH triggered, capturing data ...')
    print(f'Number of sample points: {rth.query_float("ACQ:POIN?")}')
    print(f'Data capturing elapsed time: {stop - start:.3f}sec')

    # get binary data
    start = time()
    rth.write_str("FORMat:DATA INT,16")
    rth.bin_int_numbers_format = BinIntFormat.Integer16_2bytes
    rth.data_chunk_size = 100000  # transfer in blocks of 100k bytes (default)
    data_bin = rth.query_bin_or_ascii_int_list("CHAN:DATA?")

    ch1_scale = rth.query_float("CHAN1:SCAL?")
    ch1_offs = rth.query_float("CHAN1:OFFS?")
    ch1_pos = rth.query_float("CHAN1:POS?")

    # see RTH manual for details -> Transfer of Waveform Data
    factor = ch1_scale * 8 / (255*256)
    offs = ch1_offs - ch1_pos * ch1_scale
    # apply multiplication factor and offset to the raw ADC values
    data_bin = [(x * factor + offs) for x in data_bin]

    print(f'Binary waveform transfer elapsed time: {time() - start:.3f}sec')

    plt.figure(1)
    plt.plot(data_bin)
    plt.title('Binary waveform')

    # get ASCII data
    start = time()
    rth.write_str("FORM:DATA ASC")
    rth.data_chunk_size = 100000  # transfer in blocks of 100k bytes (default)
    data_asc = rth.query_bin_or_ascii_float_list("CHAN:DATA?")

    print(f'ASCII waveform transfer elapsed time: {time() - start:.3f}sec')

    plt.figure(2)
    plt.plot(data_asc)
    plt.title('ASCII waveform')

    # get screenshot
    file_path_instr = r'/media/SD/Rohde-Schwarz/RTH/Screenshots/Device_Screenshot.png'
    file_path_pc = r'c:\temp\Device_Screenshot.png'
    
    rth.write_str("HCOP:LANG PNG")
    rth.write_str(f"MMEM:NAME '{file_path_instr}'")
    rth.write_str_with_opc("HCOP:IMM")
    rth.read_file_from_instrument_to_pc(file_path_instr, file_path_pc)
    
    rth.close()
    plt.show()


if __name__ == "__main__":
    main()
