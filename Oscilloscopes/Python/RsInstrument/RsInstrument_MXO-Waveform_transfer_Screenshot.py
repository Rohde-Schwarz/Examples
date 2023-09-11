"""
# GitHub examples repository path: Oscilloscopes/Python/RsInstrument

This Python example shows how to transfer waveform data (ASCII and binary format)
+ screenshot from MXO oscilloscope to the controller PC. The MXO probe compensation
signal can be used for a simple test.

Preconditions:
- Installed RsInstrument Python module from pypi.org
- Installed VISA e.g. R&S Visa 5.12.x or newer

Tested with:
- MXO, FW: v1.3.2.0
- Python 3.9
- RsInstrument 1.53.0

Author: R&S Customer Support /  Changes to MXO PJ
Updated on 04.05.2023
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
    # mxo = None
    try:
        # Adjust the VISA Resource string to fit your instrument
        mxo = RsInstrument('TCPIP::10.205.0.159::INSTR', id_query=True, reset=True, options="SelectVisa='rs'")
        mxo.logger.mode = LoggingMode.On
        mxo.visa_timeout = 6000  # Timeout for VISA Read Operations
        mxo.opc_timeout = 3000  # Timeout for opc-synchronised operations
        mxo.instrument_status_checking = True  # Error check after each command
    except Exception as ex:
        print('Error initializing the instrument session:\n' + ex.args[0])
        exit()

    print(f'Device IDN: {mxo.idn_string}')
    print(f'Device Options: {",".join(mxo.instrument_options)}\n')

    # Basic settings - To test with mxo probe compensation signal connected to CH1
    mxo.write('SYSTem:DISPlay:UPDate ON')  # Keep display on while under remote control
    mxo.write_with_opc('AUToscale', 10000)  # Perform autoscaling on the used signal, timeout 10 seconds
    mxo.write('TRIGger:MODE NORMal')  # Set trigger to Normal to avoid unwanted triggering while in Auto mode

    # Perform acquisition
    start = time()
    mxo.write_str_with_opc("RUNsingle")  # Single acquisition is presupposition for retrieving waveform data
    stop = time()
    print('MXO triggered, capturing data ...')
    print(f'Number of sample points: {mxo.query_float("ACQ:POIN?")}')
    print(f'Data capturing elapsed time: {stop - start:.3f}sec\n')

    # Get and plot binary data
    start = time()
    mxo.write_str("FORMat:DATA REAL,32;:FORMat:BORDer LSBFirst")
    mxo.bin_float_numbers_format = BinFloatFormat.Single_4bytes
    mxo.data_chunk_size = 100000  # transfer in blocks of 100k bytes (default)
    print('Now start to transfer binary waveform data. Please wait for about 20 seconds...')
    data_bin = mxo.query_bin_or_ascii_float_list("CHAN:DATA?")

    print(f'Binary waveform transfer elapsed time: {time() - start:.3f}sec\n')

    plt.figure(1)
    plt.plot(data_bin)
    plt.title('Binary waveform')

    # Get and plot ASCII data just to show how long it would take in comparison
    start = time()
    mxo.write_str("FORM:DATA ASC")
    mxo.data_chunk_size = 100000  # transfer in blocks of 100k bytes (default)
    print('Now start to transfer ASCII waveform data. Please wait for about 120 seconds...')
    data_asc = mxo.query_bin_or_ascii_float_list("CHAN:DATA?")
    print(f'ASCII waveform transfer elapsed time: {time() - start:.3f}sec')
    plt.figure(2)
    plt.plot(data_asc)
    plt.title('ASCII waveform')

    # get screenshot
    file_path_instr = r'/home/instrument/userData/Device_Screenshot.png'  # MXO is a LINUX based device
    file_path_pc = r'c:\temp\Device_Screenshot.png'  # While this path is based on the WIN world

    mxo.write_str("HCOPy:DEVice1:LANGuage PNG")
    mxo.write_str(f"MMEMory:NAME '{file_path_instr}'")
    mxo.write_str_with_opc("HCOPy:IMMediate1")
    mxo.read_file_from_instrument_to_pc(file_path_instr, file_path_pc)
    print(f'\nTransferred screen shot to {file_path_pc}\n')

    mxo.close()
    print('Close the plot windows to end the script...')
    plt.show()


if __name__ == "__main__":
    main()
