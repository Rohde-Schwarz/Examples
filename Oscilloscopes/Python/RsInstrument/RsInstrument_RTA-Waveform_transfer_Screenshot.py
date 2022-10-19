"""
# GitHub examples repository path: Oscilloscopes/Python/RsInstrument

This Python example shows how to transfer waveform data (ASCII and binary format)
+ screenshot from RTA oscilloscope to the controller PC. The RTA probe compensation
signal can be used for a simple test.

Preconditions:
# - Installed RsInstrument Python module from pypi.org
- Installed VISA e.g. R&S Visa 5.12.x or newer

Tested with:
- RTA4004, FW: v1.700S
- Python 3.9
- RsInstrument 1.53.0

Author: R&S Customer Support / Changes to RTA PJ
Updated on 19.10.2022
Version: v1.0

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
    RsInstrument.assert_minimum_version('1.53.0')
    rta = None
    try:
        # adjust the VISA Resource string to fit your instrument
        rta = RsInstrument('TCPIP::10.205.0.18::INSTR', True, False)
        # rta = RsInstrument('USB0::0x0AAD::0x012F::1317.5000K02/103176::INSTR', True, False)
        rta.logger.log_to_udp = True
        rta.logger.mode = LoggingMode.On
        rta.visa_timeout = 10000  # Timeout for VISA Read Operations
        rta.opc_timeout = 3000  # Timeout for opc-synchronised operations
        rta.instrument_status_checking = True  # Error check after each command
    except Exception as ex:
        print('Error initializing the instrument session:\n' + ex.args[0])
        exit()

    print(f'Device IDN: {rta.idn_string}')
    print(f'Device Options: {",".join(rta.instrument_options)}\n')

    rta.clear_status()
    rta.reset()

    # basic settings - to test with rta probe compensation signal
    rta.write_str("TIM:SCAL 0.001")
    rta.write_str("CHAN1:SCAL 0.02")
    rta.write_str("CHAN1:POS -2.5")
    rta.write('TRIGger:A:MODE NORMal')

    start = time()
    rta.write_str_with_opc("RUN")
    stop = time()
    print('rta triggered, capturing data ...')
    print(f'Number of sample points: {rta.query_float("ACQ:POIN?")}')
    print(f'Data capturing elapsed time: {stop - start:.3f}sec')

    # get binary data
    start = time()
    rta.write_str("FORMat:DATA REAL,32")
    rta.bin_float_numbers_format = BinFloatFormat.Single_4bytes_swapped
    rta.data_chunk_size = 100000  # transfer in blocks of 100k bytes (default)
    data_bin = rta.query_bin_or_ascii_float_list("CHAN1:DATA?")

    print(f'Binary waveform transfer elapsed time: {time() - start:.3f}sec')

    plt.figure(1)
    plt.plot(data_bin)
    plt.title('Binary waveform')

    """
    # get binary data - alternative way
    start = time()
    rta.write_str("FORMat:DATA REAL,32;:FORMat:BORDer LSBFirst")
    rta.query_opc()
    rta.bin_float_numbers_format = BinFloatFormat.Single_4bytes
    rta.data_chunk_size = 100000  # transfer in blocks of 100k bytes (default)
    data_bin = rta.query_bin_or_ascii_float_list("CHAN1:DATA?")

    print(f'Binary waveform transfer elapsed time: {time() - start:.3f}sec')

    plt.figure(1)
    plt.plot(data_bin)
    plt.title('Binary waveform')
    """

    # get ASCII data
    start = time()
    rta.write_str("FORM:DATA ASC")
    rta.data_chunk_size = 100000  # transfer in blocks of 100k bytes (default)
    data_asc = rta.query_bin_or_ascii_float_list("CHAN1:DATA?")

    print(f'ASCII waveform transfer elapsed time: {time() - start:.3f}sec')

    plt.figure(2)
    plt.plot(data_asc)
    plt.title('ASCII waveform')

    # get screenshot
    file_path_instr = r'/INT/DATA'
    file_name_instr = "devscrsh"
    file_type_instr = "PNG"
    file_path_pc = r'c:\temp\Device_Screenshot.png'

    rta.write_str(f"HCOP:LANG {file_type_instr}")
    rta.write_str(f"MMEMory:CDIRectory '{file_path_instr}'")
    rta.write_str(f"MMEM:NAME '{file_name_instr}'")
    rta.write_str_with_opc("HCOP:IMM")
    rta.read_file_from_instrument_to_pc(file_path_instr, file_path_pc)
    # Delete instrument file after operation is complete to avoid errors @ next script execution
    rta.query_opc()
    rta.write_str(f"MMEMory:DELete '{file_name_instr}.{file_type_instr}'")

    print(f"\nSaved screenshot to {file_path_pc}")

    rta.close()
    plt.show()


if __name__ == "__main__":
    main()
