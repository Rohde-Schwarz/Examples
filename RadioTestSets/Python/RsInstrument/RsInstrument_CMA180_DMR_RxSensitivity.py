"""
# GitHub examples repository path: RadioTestSets/Python/RsInstrument

Created on 2022/05

Author: Jahns_P
Version Number: 1
Date of last change: 2022/05/04
Requires: CMA180 with adequate options, FW 1.7.20 or newer

Description: Example for automated DMR RX Sensitivity measurement using audio feedback
             Due to blind times during the measurement, we recommend that one person also monitors the recording of the
             uninterrupted 10-second interval. In this case, the script should be expanded to include a way to manually
             increase the HF level.

General Information:
Please always check this example script for unsuitable setting that may
destroy your DUT before connecting it to the instrument!
This example does not claim to be complete. All information has been
compiled with care. However, errors can not be ruled out.
"""

# --> Import necessary packets
from RsInstrument import *
from time import sleep
from time import time

RfStartLevel = -100
RfFreq = '430.300 MHz'
Atten = '0.6 dB'
DmrAddr = '12345678'
MinAudLevel = 0.04
MaxAudLevel = 1.5

cma = RsInstrument('TCPIP::10.205.0.30::hislip0', reset=True, id_query=True,
                   options="SelectVisa='rs' , LoggingMode = Off, LoggingToConsole = False")


def meas_prep():
    """Prepare CMA to provide a DMR signal"""
    cma.write_str('SYSTem:DISPlay:UPDate ON')  # Enables to watch the CMA display while remote control
    cma.write(f'SOURce:AFRF:GENerator1:RFSettings:EATTenuation {Atten}')  # Set cable attenuation
    cma.write_str('CONFigure:BASE:SCENario DRXT')  # Scenario is Digital RX Test
    cma.write('SOURce:AFRF:GENerator1:RFSettings:CONNector RFCom')  # Use the RFCOM for measurement
    cma.write(f'SOURce:AFRF:GENerator1:RFSettings:FREQuency {RfFreq}')  # Set working frequency
    cma.write(f'SOURce:AFRF:GENerator1:RFSettings:LEVel {RfStartLevel} dBm')  # Define RF level for start
    cma.write('SOURce:AFRF:GENerator1:DSOurce DMR')  # Change mode to DMR
    cma.write('SOURce:AFRF:GENerator1:DMR:CCODe 1')   # Set Color Code to 1
    cma.write(f'SOURce:AFRF:GENerator1:DMR:SADDress {DmrAddr}')  # Define a DMR transmitter ID
    cma.write('SOURce:AFRF:GENerator1:DMR:PATTern P1031')  # Use the 1031 Hz pattern for measurement
    cma.write('CONFigure:BASE:SOUNd:SOURce AFON')  # Set system sound source to AF1 and AF2 IN
    cma.write('CONFigure:BASE:SPEaker ON')  # Enable system speaker
    cma.write('CONFigure:BASE:CMASound:VOLume 10')  # Change speaker volume
    cma.write('SOURce:AFRF:GENerator1:RFSettings:RF:ENABle ON')  # Enable RF generator (output is still OFF)
    cma.write('SOURce:AFRF:GENerator1:STATe ON')  # Enable RF generator output
    cma.write_str('CONFigure:AFRF:MEASurement1:MEValuation:AF:SCOunt 20')  # Set statistic count for scalar measurement
    cma.write_str('CONFigure:AFRF:MEASurement1:MEValuation:AFFFt:SCOunt 20')  # Statistic count for spectrum measurement
    cma.query_opc()  # CHeck for command completion of all commands sent before


def audlevel():
    """Check and adjust AF signal level if necessary to have an adequate signal available"""
    valid = 0
    while valid == 0:
        cma.write_str('INITiate:AFRF:MEASurement1:MEValuation')  # Initiate AF Measurement
        cma.query_opc()  # Wait for measurement to be done
        measurands = cma.query_str('READ:AFRF:MEASurement1:MEValuation:AIN1:AFSignal:CURRent?')  # Read out data
        # As this measurement will respond with Reliability, Frequency, Level, DCLevel, we will have to split the string
        # into a list and separate the desired components.
        measurands = measurands.split(',')
        af_level = float(measurands[2])  # AF Level is 3rd part of the list (begins with 0)
        af_freq = float(measurands[1])  # AF Frequency is 2nd part of the list
        if af_level < MinAudLevel:
            print(f'Audio Signal detected at {af_freq:.2f} Hz')
            print(f'The signal level is only {af_level:.4f} V')
            print('Please increase the audio output level of your radio to at least 20 mV!')
        if af_level > MaxAudLevel:
            print(f'Audio Signal detected at {af_freq:.2f} Hz')
            print(f'The signal level is {af_level:.2f} V')
            print('Please decrease (LOWER) the audio output level of your radio to less than 1.5 V!')
        if af_level < MaxAudLevel:
            if af_level > MinAudLevel:
                print(f'Audio Signal frequency is {af_freq:.2f} Hz')
                print(f'\nThe Audio level ({af_level:.2f} V) is within a fine range now.'
                      f'PLease do not change it during the test!\n')
                valid = 1


def coarse_rf(rfstartlevel):
    """Coarse definition of RF sensitivity level"""
    valid = 0
    rflevel = rfstartlevel
    print('Adjusting coarse RF level now')
    while valid == 0:
        cma.write_str('INITiate:AFRF:MEAS:MEV')
        cma.query_opc()
        measurands = cma.query_str('READ:AFRF:MEAS:MEV:AIN1:AFSignal:CURR?')
        measurands = measurands.split(',')
        af_level = float(measurands[2])
        if af_level > MinAudLevel:
            # Decrease the RF level until no reception
            rflevel = rflevel - 10
            cma.write(f'SOURce:AFRF:GENerator1:RFSettings:LEVel {rflevel} dBm')
            cma.query_opc()
            sleep(0.1)
        else:
            print(f'Coarse RF level result is {rflevel} dBm\n')
            return rflevel


def fine_rf(rflevel):
    """Fine definition of RF sensitivity level"""
    valid = 0
    print('Adjusting fine RF level now')
    while valid == 0:
        cma.write_str('INITiate:AFRF:MEAS:MEV')
        cma.query_opc()
        measurands = cma.query_str('READ:AFRF:MEAS:MEV:AIN1:AFSignal:CURR?')
        measurands = measurands.split(',')
        af_level = float(measurands[2])
        if af_level < MinAudLevel:
            # Increase Level until first reception
            rflevel = rflevel + 1
            cma.write(f'SOURce:AFRF:GENerator1:RFSettings:LEVel {rflevel} dBm')
            cma.query_opc()
            sleep(0.1)
        else:
            print(f'First response at an RF level of {rflevel} dBm\n. Fine RF level is set now.')
            return rflevel


def measure(rflevel):
    """Measurement in a loop - find RX sensitivity level being present for at least 10 seconds"""
    valid = 0
    # Statistic count for measurements will be set to 1 to have minimum acquisition time
    cma.write_str('CONFigure:AFRF:MEASurement1:MEValuation:AF:SCOunt 1')
    cma.write_str('CONFigure:AFRF:MEASurement1:MEValuation:AFFFt:SCOunt 1')
    starttime = time()  # Use system timer to watch signal duration
    while valid == 0:
        cma.write_str('INITiate:AFRF:MEAS:MEV')
        cma.query_opc()
        measurands = cma.query_str('READ:AFRF:MEAS:MEV:AIN1:AFSignal:CURR?')
        measurands = measurands.split(',')
        af_level = float(measurands[2])
        if af_level < MinAudLevel:
            rflevel = rflevel + 0.1
            cma.write(f'SOURce:AFRF:GENerator1:RFSettings:LEVel {rflevel} dBm')
            cma.query_opc()
            sleep(0.1)
            starttime = time()
        else:
            if time() - starttime > 10:
                print(f'Signal present for at least 10 seconds at {rflevel} dBm')
                valid = 1


def close():
    """Switch off all active generators and close connection"""
    cma.write('CONFigure:BASE:SPEaker OFF')  # Disable system speaker
    cma.write('SOURce:AFRF:GENerator1:STATe OFF')  # Switch off RF generator output
    cma.close()


def main():
    meas_prep()
    audlevel()
    rflevel = coarse_rf(RfStartLevel)
    rflevel = fine_rf(rflevel)
    measure(rflevel)
    close()


main()
print("I'm done")
