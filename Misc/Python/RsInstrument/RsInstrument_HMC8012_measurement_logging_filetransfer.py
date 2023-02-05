"""

# GitHub examples repository path: Misc/Python/RsInstrument

Created on 2023/01

Author: Customer Support / PJ
Version Number: 2
Date of last change: 2023/02/05
Requires: HMC8012, FW 1.400 or newer and eventually adequate options
- Installed RsInstrument Python module 1.53.0 or newer
- Installed VISA e.g. R&S Visa 5.12.x or newer
- At least define the VISA resource string in line 33 before you start the script

Description: Setup measurement and log to a file for a certain time, transfer the log file to the PC


General Information:

Please always check this example script for unsuitable settings before connecting the instrument!
This example does not claim to be complete. All information has been
compiled with care. However, errors can not be ruled out.

Please find more information about RsInstrument at
https://rsinstrument.readthedocs.io/en/latest/
"""

# --> Import necessary packets
import os
from time import sleep
from RsInstrument import RsInstrument, TimeoutException

# Define variables
resource = 'TCPIP::10.205.0.218::INSTR'  # VISA resource string for the device
log_dur = 5  # Log time in seconds
log_file_name = 'TEST.CSV'  # Name of the HMC log file
pc_log_file_name = r'c:\Tempdata\logdata.csv'  # Name and Path of the PC log file

# Control the device via RsVISA
hmc8012 = RsInstrument(resource, reset=True, id_query=True, options="SelectVisa='rs', AddTermCharToWriteBinData = OFF, "
                                                                    "OpcQueryAfterWrite = OFF, "
                                                                    "QueryInstrumentStatus = OFF,"
                                                                    "StbInErrorCheck = OFF,"
                                                                    " DisableOpcQuery = ON, VxiCapable = OFF, "
                                                                    "VisaTimeout = 10000, OpcTimeout = 10000")


def com_prep() -> None:
    """Prepare the communication (termination, etc.)."""
    RsInstrument.assert_minimum_version('1.53.0')
    # Confirm VISA package to be chosen
    print(f'VISA Manufacturer: {hmc8012.visa_manufacturer}')
    hmc8012.clear_status()  # Clear status register


def close() -> None:
    """
    Close the VISA session.

    :return: None
    """
    hmc8012.close()


def com_check() -> None:
    """
    Check communication with the device.

    :return: None
    """
    # Check for instrument to be present
    print(f'Hello, I am {hmc8012.query_str_with_opc("*IDN?")}\n')


def meas_prep() -> None:
    """
    Prepare instrument for desired measurement
    In this case setting an adequate DC Voltage range and set ADC rate to maximum

    :return: None
    """
    hmc8012.write_str_with_opc(
        'CONF:VOLT:DC 400mV')  # DC Voltage range to 400mV
    hmc8012.write_str_with_opc('SENSe:ADCRate FAST')  # ADC rate to Fast mode


def log_setup(log_duration: int, log_file_name: str, log_format: str = 'CSV') -> None:   
    """
    Prepare and begin logging, in addition check the directory if the file exists
    after logging process is complete.

    :param log_duration: Log duration in seconds
    :param log_file_name: Name of the log file on the HMC8012
    :param log_format: Log file format, default is CSV
    :return: None
    :raises IOError: If the log file to be deleted is not present
    :raises TimeoutException: If the timeout is reached
    """

    # Delete the log file (if already existing) and insert a try block to prevent
    # throwing an error when the log file to be deleted is not present
    try:
        # Read out directory before logging (only for information)
        print(
            f'Content of the directory at the start is {hmc8012.query_str_list_with_opc("DATA:LIST? INT")}')
        # Delete the logfile if already present
        hmc8012.write_str_with_opc(f'DATA:DELETE "{log_file_name}",INT')
    except IOError:
        print('An IOError occurred while deleting the log file, continuing anyway.')
    except TimeoutException:
        print('Timeout occurred while deleting the log file, continuing anyway.')

    # hmc8012.query_opc()

    # Log mode is set to time mode
    hmc8012.write_str_with_opc('DATA:LOG:MODE TIME')
    # Set logging duration time (log_duration) in seconds
    hmc8012.write_str_with_opc(f'DATA:LOG:TIME {log_duration}')
    # Set minimal interval time (0) between the logging steps
    hmc8012.write_str_with_opc('DATA:LOG:INTerval 0')

    # CSV is log file format
    hmc8012.write_str_with_opc(f'DATA:LOG:FORMAT {log_format}')
    hmc8012.write_str_with_opc('DATA:LOG:FNAME "' + log_file_name +
                               '", INT')  # Define Log file name
    print(f'Log File Name now is {hmc8012.query("DATA:LOG:FNAME?")}')
    hmc8012.query_opc()  # Check for command completion

    hmc8012.write_str_with_opc('DATA:LOG:STATe ON ')  # Activate logging
    print(f'Logging runs now for {log_duration} seconds - please wait!\n')
    # Wait for the log to be written and add five seconds for logging to be completed
    sleep(int(log_duration + 5))


def file_get(log_file_name: str, pc_log_file_name: str, delete_log_file: bool = True) -> None:
    """
    Transfer the log file to the local PC.

    :param log_file_name: Name of the log file on the HMC8012
    :param pc_log_file_name: Name and path of the log file on the PC
    :param delete_log_file: Delete the log file on the HMC8012 after transfer
    :return: None
    """
    print('Now transferring the log file...\n')
    hmc8012.visa_timeout = 10000  # Enlarge timeout value for VISA Read Operations
    # Disable to process read termination characters
    hmc8012.get_session_handle().read_termination = ""
    # Query data into a string
    log_data = hmc8012.query_str_with_opc(
        f'DATA:DATA? "{log_file_name}",INT')
    # Ensure that the path to the file exists
    os.makedirs(os.path.dirname(pc_log_file_name), exist_ok=True)
    # Open the PC log file in write mode,
    # write the string into the file and close the file
    open(pc_log_file_name, 'w').write(log_data)
    # Switch back to process read termination character "\n"
    hmc8012.get_session_handle().read_termination = "\n"
    print(f'File saved locally to {pc_log_file_name}')

    if delete_log_file:
        # Delete the log file from the HMC8012
        hmc8012.write_str_with_opc(f'DATA:DELETE "{log_file_name}",INT')

    # Set back to original timeout value for VISA Read Operations
    hmc8012.visa_timeout = 5000


# Main Program begins here
if __name__ == '__main__':
    print("Program started.")

    com_prep()
    com_check()
    meas_prep()
    log_setup(log_duration=log_dur, log_file_name=log_file_name)
    file_get(log_file_name=log_file_name, pc_log_file_name=pc_log_file_name)
    close()

    print("Program successfully ended.")
