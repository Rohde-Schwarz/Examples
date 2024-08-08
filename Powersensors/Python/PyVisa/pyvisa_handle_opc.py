"""
# GitHub examples repository path: not known yet

This Python example shows how to deal with command completion using an R&S NRPxx power sensor or the R&S NRX.
Each part of the example performs a zero calibration followed by a single measurement.

Preconditions:
- Installed pyvisa Python module from pypi.org
- Installed VISA e.g. R&S Visa 5.12.x or newer

Tested with:
- NRP18SN, FW v02.50.2303250
, NRX, FW 02.60.24032102
- Python 3.12
- PyVISA 1.14.1

Author: R&S Product Management AE 1GP3 / PJ
Updated on 26.07.2024
Version: v1.0

Technical support -> https://www.rohde-schwarz.com/support

Before running, please always check your setup!
This example does not claim to be complete. All information have been
compiled with care. However, errors can’t be ruled out.

"""

# --> Import necessary packets
from pyvisa import *
from pyvisa import constants
from time import sleep

# Define variables
resource = 'USB::0x0AAD::0x0139::102246::INSTR'  # VISA resource string for a USB device
# resource = 'TCPIP::NRP50SN-100886::hislip0'  # VISA resource string for a hislip network device using the host name
# resource = 'TCPIP::192.168.2.100::hislip0'  # VISA resource string for a hislip network device using the IP address
# resource = 'GPIB::20::INSTR'  # VISA resource string for a GPIB device (NRX)

# Define the device handle
rm = ResourceManager()
device = rm.open_resource(resource)

# Define all the subroutines


def com_check():
    """Test the device connection, request ID as well as installed options"""
    device.write('*RST;*CLS')  # Reset, Clear Status  -> also clears the status register as consequence
    device.query('*OPC?')  # Wait for the reset to be done
    print('Hello, I am ' + device.query('*IDN?'), end=" ")
    print('and I have the following options available: \n' + device.query('*OPT?'))


def req_opc():
    """Perform zeroing using *OPC? and adequate VISA timeout setting"""
    std_tmo = device.timeout  # Read out standard timeout setting to reset it after the following procedure
    device.timeout = 10500  # Set the timeout variable to a value (in ms) that allows waiting for a successful zeroing
    print('Start zeroing with *OPC?...')
    device.write('CALibration:ZERO:AUTO ONCE')
    device.query('*OPC?')  # *OPC? only returns '1' after the last command has been successfully processed. It is
    # therefore only necessary to wait for the answer. If this happens, the zeroing is also successful.
    # Otherwise, it would come to a timeout. The typical duration of the zeroing process can be between about 5 and 10
    # seconds, according to the sensor.
    print('...Sensor is zeroed now.')
    device.timeout = std_tmo
    device.write('SENSe1:AVERage:COUNt:AUTO OFF')  # Disables the automatic averaging count for sensor 1
    device.write('SENSe1:AVERage:COUNt 1')  # Set average count to 1 (no averaging)
    device.write('INITiate:CONTinuous ON')   # Enables continuous initiation mode. The device will continuously take
    # measurements without needing a separate trigger command
    print(f'Measurement value is {device.query('FETCh?')}')  # Read and print measurement value


def req_stb():
    """Perform zeroing using the Status Byte"""
    print('Start zeroing with status byte request...')
    device.clear()  # VISA operation vi_clear()
    device.write('*ESE 1')  # Filters only bit 0 (OPC = Operation Complete) of the Event Status Register to be
    # forwarded to bit 5 of the Status Byte (ESB = Event Status register summary Bit)
    device.query('*ESR?')  # Returns the contents of the event status register and clears it on read.
    device.write('CALibration:ZERO:AUTO ONCE;*OPC')  # Command chain with ; binds the *OPC? to the zeroing command
    while True:
        stb = device.read_stb()  # Read Status Byte information
        if stb & 32 == 0:  # Only check for bit 5 of the status Byte and repeat until it did not turn to 1 (OPC)
            sleep(.5)  # Some time delay between single requests to reduce polling frequency
        else:
            break
    print('...Sensor is zeroed now.')
    device.write('SENSe1:AVERage:COUNt:AUTO OFF')  # Disables the automatic averaging count for sensor 1
    device.write('SENSe1:AVERage:COUNt 1')  # Set average count to 1 (no averaging)
    device.write('INITiate:CONTinuous ON')  # Enables continuous initiation mode. The device will continuously take
    # measurements without needing a separate trigger command
    print(f'Measurement value is {device.query('FETCh?')}')  # Read and print measurement value


def req_serv_gpib():
    """Perform zeroing using the service request feature, only for GPIB devices in pyvisa (e.g. NRX)"""
    print('Start zeroing using a service request (GPIB devices only!)...')
    device.clear()  # VISA operation vi_clear()
    device.write('*ESE 1;*SRE 32')  # Filters only bit 0 (OPC = Operation Complete) of the Event Status Register to be
    # forwarded to bit 5 of the Status Byte (ESB = Event Status register summary Bit), which is then filtered over
    # Service Request Enable @ bit 5
    device.write('*CLS')  # Clear Status  -> also clears the status byte as consequence
    device.write('CALibration1:ZERO:AUTO ONCE;*OPC')
    device.wait_for_srq(11500)  # Start the waiting process checking if a Service Request as been triggered. The typical
    # duration of the zeroing process can be between about 5 and 10 seconds, according to the sensor.
    print('...Sensor is zeroed now.')
    device.write('SENSe1:AVERage:COUNt:AUTO OFF')  # Disables the automatic averaging count for sensor 1
    device.write('SENSe1:AVERage:COUNt 1')  # Set average count to 1 (no averaging)
    device.write('INITiate:CONTinuous ON')  # Enables continuous initiation mode. The device will continuously take
    # measurements without needing a separate trigger command
    print(f'Measurement value is {device.query('FETCh?')}')  # Read and print measurement value


def req_won_event():
    """Perform zeroing waiting for a service request event"""
    event_type = constants.EventType.service_request  # Type to trigger an event
    event_mech = constants.EventMechanism.queue  # Mechanism by which we want to be notified
    print('Start zeroing waiting for a service request event...')
    device.clear()
    device.write('*ESE 1;*SRE 32')  # Filters only bit 0 (OPC = Operation Complete) of the Event Status Register to be
    # forwarded to bit 5 of the Status Byte (ESB = Event Status register summary Bit), which is then filtered over
    # Service Request Enable @ bit 5
    device.write('*CLS')  # Clear Status  -> also clears the status byte as consequence
    device.enable_event(event_type, event_mech)  # Enable polling for the event
    device.write('CALibration:ZERO:AUTO ONCE;*OPC')
    device.wait_on_event(event_type, 10500)  # Start the waiting process. The typical duration of the zeroing
    # process can be between about 5 and 10 seconds, according to the sensor.
    device.disable_event(event_type, event_mech)  # Disable polling.
    print('...Sensor is zeroed now.')
    device.write('SENSe1:AVERage:COUNt:AUTO OFF')  # Disables the automatic averaging count for sensor 1
    device.write('SENSe1:AVERage:COUNt 1')  # Set average count to 1 (no averaging)
    device.write('INITiate:CONTinuous ON')  # Enables continuous initiation mode. The device will continuously take
    # measurements without needing a separate trigger command
    print(f'Measurement value is {device.query('FETCh?')}')  # Read and print measurement value


def close():
    """Close the VISA session"""
    device.close()


#  Main program begins here
com_check()
req_opc()
req_stb()
# req_serv_gpib()
req_won_event()
close()

print("Program successfully ended.")
