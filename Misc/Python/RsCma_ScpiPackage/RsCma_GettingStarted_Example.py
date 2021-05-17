# Example of using R&S CMA180 auto-generated instrument driver module RsCma for Python 3

from RsCma import *  # install from pypi.org

RsCma.assert_minimum_version('1.5.70')
cma = RsCma('TCPIP::10.112.1.116::INSTR', True, False)
print(f'CMA Identification: {cma.utilities.idn_string}')

# SYSTem:DISPlay:UPDate
cma.system.display.set_update(False)

# SOURce:AFRF:GEN:STATe
cma.source.afRf.generator.state.set(True)

# SOURce:AFRF:GEN:RFSettings:FREQuency
cma.source.afRf.generator.rfSettings.set_frequency(100E3)

# SOURce:AFRF:GEN:RFSettings:LEVel
cma.source.afRf.generator.rfSettings.set_level(-20.0)

# CONFigure:GPRF:MEAS:SPECtrum:FREQuency:SPAN:MODE
cma.configure.gprfMeasurement.spectrum.frequency.span.set_mode(enums.SpanMode.FSWeep)

# CONFigure:GPRF:MEAS:SPECtrum:SCOunt
cma.configure.gprfMeasurement.spectrum.set_scount(10)

# CONFigure:GPRF:MEAS:SPECtrum:REPetition
cma.configure.gprfMeasurement.spectrum.set_repetition(enums.Repeat.SINGleshot)

# CONFigure:GPRF:MEAS:SPECtrum:FREQuency:SPAN
cma.configure.gprfMeasurement.spectrum.frequency.span.set_value(1.1E6)

# CONFigure:GPRF:MEAS:SPECtrum:FREQuency:CENTer
cma.configure.gprfMeasurement.spectrum.frequency.set_center(100E3)

# INITiate:GPRF:MEAS:SPECtrum
cma.gprfMeasurement.spectrum.initiate()
cma.gprfMeasurement.spectrum.initiate_with_opc()

# READ:GPRF:MEAS:POWer:CURRent?
results_power = cma.gprfMeasurement.power.current.read()

# FETCh:GPRF:MEAS:SPECtrum:RMS:CURRent?
results_spectrum = cma.gprfMeasurement.spectrum.rms.current.fetch()

# SOURce:AFRF:GENerator:IGENerator<nr>:MTONe:TONE<no>:ENABle
# option A: stating all the repcaps in the method call
# sends: SOURce:AFRF:GENerator:IGENerator2:MTONe:TONE4:ENABle ON
cma.source.afRf.generator.internalGenerator.multiTone.tone.enable.set(True, repcap.InternalGen.Nr2, repcap.ToneNumber.Nr4)

# option B - setting default values of the repcaps in the groups:
cma.source.afRf.generator.internalGenerator.repcap_internalGen_set(repcap.InternalGen.Nr2)
cma.source.afRf.generator.internalGenerator.multiTone.tone.repcap_toneNumber_set(repcap.ToneNumber.Nr4)

# Then use the method call without defining the repcaps - they stay at the default value
# sends: SOURce:AFRF:GENerator:IGENerator2:MTONe:TONE4:ENABle ON
cma.source.afRf.generator.internalGenerator.multiTone.tone.enable.set(True)

# cloning instances:
igen3 = cma.source.afRf.generator.internalGenerator.clone()
igen3.repcap_internalGen_set(repcap.InternalGen.Nr3)
igen3.multiTone.tone.enable.set(True)
# sends: SOURce:AFRF:GENerator:IGENerator3:MTONe:TONE4:ENABle ON

igen3.multiTone.tone.repcap_toneNumber_set(repcap.ToneNumber.Nr7)
# sends: SOURce:AFRF:GENerator:IGENerator3:MTONe:TONE7:ENABle ON

cma.close()
