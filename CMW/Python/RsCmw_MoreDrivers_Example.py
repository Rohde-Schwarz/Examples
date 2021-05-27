"""
Example on how to use more than one Python RsCmw auto-generated instrument drivers for R&S CMW 500
(Base and GPRF Measurement and Generator) in one script with shared VISA session
"""

from RsCmwBase import RsCmwBase  # install from pypi.org
from RsCmwBase import enums as enums_base
from RsCmwBase import repcap as repcap_base

from RsCmwGprfMeas import RsCmwGprfMeas  # install from pypi.org
from RsCmwGprfMeas import enums as enums_gprf_meas
from RsCmwGprfMeas import repcap as repcap_gprf_meas

from RsCmwGprfGen import RsCmwGprfGen  # install from pypi.org
from RsCmwGprfGen import enums as enums_gprf_gen
from RsCmwGprfGen import repcap as repcap_gprf_gen

RsCmwBase.assert_minimum_version('3.7.90.38')
RsCmwGprfMeas.assert_minimum_version('3.7.30.31')
RsCmwGprfGen.assert_minimum_version('3.7.50.53')

cmw_base = RsCmwBase('TCPIP::10.112.1.116::INSTR', True, False)
# Reference Frequency Source
# SCPI Command: SYSTem:BASE:REFerence:FREQuency:SOURce
cmw_base.system.reference.frequency.set_source(enums_base.SourceIntExt.INTernal)

cmw_gprf_meas = RsCmwGprfMeas.from_existing_session(cmw_base)

# SCPI Command: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:FREQuency:CENTer
cmw_gprf_meas.configure.spectrum.frequency.set_center(100E6)
# Setting a global repcap
cmw_gprf_meas.repcap_instance_set(repcap_gprf_meas.Instance.Inst1)

cmw_gprf_gen = RsCmwGprfGen.from_existing_session(cmw_base)
cmw_gprf_gen.repcap_instance_set(repcap_gprf_gen.Instance.Inst1)

cmw_base.utilities.write_str("*RST")
cmw_base.utilities.instrument_status_checking = True

# Only close the session that was opened separately
cmw_base.close()
