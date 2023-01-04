"""
# GitHub examples repository path: CMXP/Python/RsCmxp_xxx_ScpiPackages

Example from the CMP UWB user manual 'Specifying General and Common Measurement Settings'
Configure RF and analyzer settings:
Input signal path, external attenuation, carrier center frequency, expected peak power and user margin.
"""

from RsCMPX_UwbMeas import *  # install from pypi.org

RsCMPX_UwbMeas.assert_minimum_version('4.0.7')

cmp = RsCMPX_UwbMeas('TCPIP::10.112.1.116::INSTR')
print(f'CMW Base IND: {cmp.utilities.idn_string}')
print(f'CMW Instrument options:\n{",".join(cmp.utilities.instrument_options)}')
cmp.utilities.visa_timeout = 5000

# Sends OPC after each command
cmp.utilities.opc_query_after_write = False

# Checks for syst:err? after each command / query
cmp.utilities.instrument_status_checking = True

# Display all the available signal paths
paths = cmp.catalog.uwbMeas.get_spath()
print('Available Signal Paths:')
for x in paths:
    print(x)
print('\n')

# Set instance ROUTe:UWB:MEAS<i> to 1
cmp.repcap_instance_set(repcap.Instance.Inst1)

#   ROUTe:UWB:MEAS:SPATh 'Port1.RRH.RF1'
cmp.route.uwbMeas.set_spath('Port1.RRH.RF1')

#   CONFigure:UWB:MEAS:RFSettings:EATTenuation 2
cmp.configure.uwbMeas.rfSettings.set_eattenuation(2)


#   CONFigure:UWB:MEAS:RFSettings:CHANnel 5
cmp.configure.uwbMeas.rfSettings.set_channel(5)

# CONFigure:UWB:MEAS:RFSettings:FREQuency 6.4896E+9
cmp.configure.uwbMeas.rfSettings.set_frequency(6.4896E+9)

# CONFigure:UWB:MEAS:RFSettings:ENPower 7
cmp.configure.uwbMeas.rfSettings.set_envelope_power(7)

# CONFigure:UWB:MEAS:RFSettings:UMARgin 5
cmp.configure.uwbMeas.rfSettings.set_umargin(7)

# Close the session
cmp.close()
