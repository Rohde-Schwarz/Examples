"""
# GitHub examples repository path: Oscilloscopes/Python/RsInstrument

This Python example shows how to transfer waveform data (ASCII and binary format)
+ screenshot from RTO oscilloscope to the controller PC. The RTO probe compensation
signal can be used for a simple test.

Preconditions:
- Installed RsInstrument Python module from pypi.org
- Installed VISA e.g. R&S Visa 5.12.x or newer

Tested with:
- RTO, FW: v4.80.1.0
- Python 3.9
- RsInstrument 1.53.0

Author: R&S Customer Support /  Changes to RTO PJ
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
    rto = None
    try:
        # Adjust the VISA Resource string to fit your instrument
        rto = RsInstrument('TCPIP::10.205.0.103::INSTR', True, False)
        # rto.logger.mode = LoggingMode.On
        rto.visa_timeout = 6000  # Timeout for VISA Read Operations
        rto.opc_timeout = 3000  # Timeout for opc-synchronised operations
        rto.instrument_status_checking = True  # Error check after each command
    except Exception as ex:
        print('Error initializing the instrument session:\n' + ex.args[0])
        exit()

    print(f'Device IDN: {rto.idn_string}')
    print(f'Device Options: {",".join(rto.instrument_options)}\n')

    rto.clear_status()
    rto.reset()

    # Basic settings - to test with RTO probe compensation signal
    rto.write('AUToscale')  # Perform autoscaling on the used signal
    rto.write('TRIGger:MODE AUTO')

    start = time()
    rto.write_str_with_opc("RUNsingle")
    stop = time()
    print('RTO triggered, capturing data ...')
    print(f'Number of sample points: {rto.query_float("ACQ:POIN?")}')
    print(f'Data capturing elapsed time: {stop - start:.3f}sec')

    # Get and plot binary data
    start = time()
    rto.write_str("FORMat:DATA REAL,32;:FORMat:BORDer LSBFirst")
    rto.bin_float_numbers_format = BinFloatFormat.Single_4bytes
    rto.data_chunk_size = 100000  # transfer in blocks of 100k bytes (default)
    data_bin = rto.query_bin_or_ascii_float_list("CHAN:DATA?")

    """
    # Alternative way to get and plot binary data
    
    start = time()
    rto.write_str("FORMat:DATA REAL,32")
    rto.bin_float_numbers_format = BinFloatFormat.Single_4bytes_swapped
    rto.data_chunk_size = 100000  # transfer in blocks of 100k bytes (default)
    data_bin = rto.query_bin_or_ascii_float_list("CHAN:DATA?")
    """

    print(f'Binary waveform transfer elapsed time: {time() - start:.3f}sec')

    plt.figure(1)
    plt.plot(data_bin)
    plt.title('Binary waveform')

    # Get and plot ASCII data just to show how long it would take in comparison
    start = time()
    rto.write_str("FORM:DATA ASC")
    rto.data_chunk_size = 100000  # transfer in blocks of 100k bytes (default)
    data_asc = rto.query_bin_or_ascii_float_list("CHAN:DATA?")
    print(f'ASCII waveform transfer elapsed time: {time() - start:.3f}sec')
    plt.figure(2)
    plt.plot(data_asc)
    plt.title('ASCII waveform')

    # get screenshot
    file_path_instr = r'c:\Temp\Device_Screenshot.png'
    file_path_pc = r'c:\temp\Device_Screenshot.png'

    rto.write_str("HCOPy:DEVice1:LANGuage PNG")
    rto.write_str(f"MMEMory:NAME '{file_path_instr}'")
    rto.write_str_with_opc("HCOPy:IMMediate1")
    rto.read_file_from_instrument_to_pc(file_path_instr, file_path_pc)
    print(f'\nTransferred screen shot to {file_path_pc}')

    rto.close()
    plt.show()


if __name__ == "__main__":
    main()
