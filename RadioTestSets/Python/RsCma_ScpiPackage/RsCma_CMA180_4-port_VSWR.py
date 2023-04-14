# -*- coding: utf-8 -*-
"""
Created on 2023/04

Author: Customer Support / PJ
Version Number: 1
Date of last change: 2023/04/05
Requires: R&S CMA180, FW 1.7.20 or newer
- Installed RsCma Python module (see https://rscma.readthedocs.io/en/latest/)
- Installed VISA e.g. R&S Visa 5.12.x or newer
- Directional coupler with 4 ports
    - IN = RF out
    - OUT = DUT
    - FWD = RF COM
    - REFL = RF IN

Description: Initiate Instrument, get FWD and REFL curve data,
calculate VSWR based on the formula VSWR = (UFWD+UREFL)/(UFWD-UREFL),
plot SWR data over frequency.


General Information:
This example does not claim to be complete. All information has been
compiled with care. However, errors can not be ruled out.
"""

from RsCma import *
from numpy import sqrt
from numpy import array
import matplotlib.pyplot as plt

RsCma.assert_minimum_version('1.7.20')  # Check for minimum RsCma plugin version
cma = RsCma('TCPIP::10.205.0.34::hislip0', True, True, "SelectVisa='rs',")  # Init with IDN query and reset and
# control the device via RsVISA

idn = cma.utilities.idn_string  # Request and display instrument identification
print(f"\nHello, I am '{idn}'")

cma.system.display.set_update(True)  # Switch on display whilst under remote control


def meas_setup():
    """Set up the measurement: Spectrum Analyzer Mode, set generator to RF OUT"""
    cma.configure.base.set_scenario(scenario=enums.BaseScenario.SPECtrum)
    cma.utilities.query_opc()  # Wait for "Operation Complete" after switching scenario
    cma.source.afRf.generator.rfSettings.set_connector(output_connector=enums.OutputConnector.RFOut)
    cma.source.afRf.generator.rfSettings.set_level(0)  # Set output power to 0 dBm
    cma.configure.gprfMeasurement.spectrum.set_scount(10)  # Set number of statistic counts
    cma.configure.gprfMeasurement.spectrum.set_repetition(enums.Repeat.SINGleshot)
    cma.configure.gprfMeasurement.spectrum.frequency.span.set_value(0.6E9)
    cma.configure.gprfMeasurement.spectrum.frequency.set_center(2.45E9)
    cma.configure.gprfMeasurement.rfSettings.set_envelope_power(exp_nominal_power=-10)
    cma.configure.gprfMeasurement.spectrum.freqSweep.rbw.set_auto(rbw_auto=False)
    cma.configure.gprfMeasurement.spectrum.freqSweep.rbw.set_value(rbw=100E3)
    cma.configure.gprfMeasurement.spectrum.tgenerator.set_enable(True)  # Enable tracking generator
    cma.configure.gprfMeasurement.spectrum.frequency.span.set_mode(enums.SpanMode.FSWeep)
    print('Setup is done so far...')


def meas_fwd():
    """Define according connector, perform forward power measurement and fetch trace data."""
    cma.configure.gprfMeasurement.rfSettings.set_connector(input_connector=enums.InputConnector.RFCom)
    cma.gprfMeasurement.spectrum.initiate()
    cma.utilities.query_opc()
    cma.utilities.visa_timeout = 30000
    fwd_values = cma.gprfMeasurement.spectrum.maximum.maximum.fetch()
    cma.utilities.visa_timeout = 3000
    return fwd_values


def meas_rev():
    """Define according connector, perform reflected power measurement and fetch trace data"""
    cma.configure.gprfMeasurement.rfSettings.set_connector(input_connector=enums.InputConnector.RFIN)
    cma.gprfMeasurement.spectrum.initiate()
    cma.utilities.query_opc()
    cma.utilities.visa_timeout = 30000
    rev_values = cma.gprfMeasurement.spectrum.maximum.maximum.fetch()
    cma.utilities.visa_timeout = 3000
    return rev_values


def get_freq():
    """Fetch frequency list"""
    cma.utilities.visa_timeout = 30000
    freq_list = cma.gprfMeasurement.spectrum.freqSweep.xvalues.fetch()
    cma.utilities.visa_timeout = 3000
    return freq_list


def calc_swr():
    """Start the sub functions and finally calculate SWR data list"""
    print('Begin to collect forward power curve data...')
    fwd_db = array(meas_fwd())
    print('Begin to collect reflected power curve data...')
    rev_db = array(meas_rev())
    print('Get according frequency data...')
    freq_list = array(get_freq())
    """Perform forward power measurement and fetch trace data"""
    print('SWR calculation...', end='')
    fwd_mw = 10 ** (fwd_db / 10)
    rev_mw = 10 ** (rev_db / 10)
    swr_list = (sqrt(fwd_mw + rev_mw) / sqrt(fwd_mw - rev_mw))
    print(' is done now.')
    plt.title('SWR over frequency')
    plt.figure(1)
    plt.plot(freq_list, swr_list)
    plt.xlabel('Frequency')
    plt.ylabel('SWR')
    plt.show()


def close():
    """Close VISA connection"""
    cma.close()  # Close the connection finally


# Main
meas_setup()
calc_swr()
close()

print('\n --> I am done now')
