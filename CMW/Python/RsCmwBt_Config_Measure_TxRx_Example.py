""" Simple example of using R&S CMW500 auto-generated instrument driver module RsCmwBt for Python 3
	The SCPI sequence is taken from the example in the CMW_Bluetooth_UserManual_V3-8-20_en_39.pdf pages:
	- Bluetooth Measurements > Programming > Tx-Rx Measurements > Configuring a Tx-Rx Measurement
	- Bluetooth Measurements > Programming > Tx-Rx Measurements > Performing a Tx-Rx Measurement
"""

from RsCmwBluetoothMeas import *  # install from pypi.org

RsCmwBluetoothMeas.assert_minimum_version('3.7.90.18')
cmw_btm = RsCmwBluetoothMeas('TCPIP::10.112.1.116::INSTR', True, False)
print(f'CMW Identification: {cmw_btm.utilities.idn_string}')

# You can still use the direct SCPI write / query:
cmw_btm.utilities.write_str('*RST')
instr_options = cmw_btm.utilities.query_str('*OPT?')

# ******************************************************************************************************************************************************************
# Configuring a Tx-Rx Measurement
# ******************************************************************************************************************************************************************

# *********************************************************************************
# System-Reset
# *********************************************************************************
cmw_btm.utilities.reset()
# *********************************************************************************
# Initial configuration to create temporary ARB file: set automatic
# detection, specify routing, set burst type LE, PHY LE1M, advertiser
# packet type. Specify advertiser channel frequency, or alternatively
# channel index. Set no measurement stop condition, disable
# measure on exception, enable only PvT and modulation
# views, set modulation and PvT statistic count to 1, set instrument
# address and address type. Enable ARB generation and start Tx measurement.
# *********************************************************************************

# The part 'BLUetooth:MEAS' is left out to make the API shorter - it is repeated in all the BT Measurement commands
# CONFigure:BLUetooth:MEAS:ISIGnal:DMODe AUTO
cmw_btm.configure.inputSignal.set_dmode(enums.AutoManualMode.AUTO)

# The command accepts two parameters, that are given over as structure - instance of a class SaloneStruct() with two fields RxConnector and RxConverter
# ROUTe:BLUetooth:MEAS:SCENario:SALone R11,RX11
routing = cmw_btm.route.scenario.SaloneStruct()
routing.Rx_Connector = enums.RxConnector.R11
routing.Rf_Converter = enums.RxConverter.RX11
cmw_btm.route.scenario.set_salone(routing)

# CONFigure:BLUetooth:MEAS:ISIGnal:BTYPe LE
cmw_btm.configure.inputSignal.set_btype(enums.BurstType.LE)

# CONFigure:BLUetooth:MEAS:ISIGnal:LENergy:PHY LE1M
cmw_btm.configure.inputSignal.lowEnergy.set_phy(enums.LePhysicalType.LE1M)

# CONFigure:BLUetooth:MEAS:ISIGnal:PTYPe:LENergy:LE1M ADV
cmw_btm.configure.inputSignal.ptype.lowEnergy.set_le1m(enums.LePacketType.ADVertiser)

# CONFigure:BLUetooth:MEAS:RFSettings:FREQuency 2402
cmw_btm.configure.rfSettings.set_frequency(2402)

# CONFigure:BLUetooth:MEAS:RXQuality:AINDex 37
cmw_btm.configure.rxQuality.set_aindex(37)

# CONFigure:BLUetooth:MEAS:MEValuation:SCONdition NONE
cmw_btm.configure.multiEval.set_scondition(enums.StopCondition.NONE)

# CONFigure:BLUetooth:MEAS:MEValuation:MOEXception OFF
cmw_btm.configure.multiEval.set_moexception(False)

# CONFigure:BLUetooth:MEAS:TRX:RESult:ALL ON,ON,ON,ON
trx_result = cmw_btm.configure.trx.result.AllStruct()
trx_result.Spot_Check = True
trx_result.Power = True
trx_result.Modulation = True
trx_result.Spectrum_Acp = True
cmw_btm.configure.trx.result.set_all(trx_result)

# CONFigure:BLUetooth:MEAS:MEValuation:SCOunt:MODulation 1
cmw_btm.configure.multiEval.scount.set_modulation(1)

# CONFigure:BLUetooth:MEAS:MEValuation:SCOunt:PVTime 1
cmw_btm.configure.multiEval.scount.set_powerVsTime(1)

# CONFigure:BLUetooth:MEAS:RXQuality:SADDress #H1234
cmw_btm.configure.rxQuality.set_saddress('#H1234')

# CONFigure:BLUetooth:MEAS:RXQuality:SATYpe PUBL
cmw_btm.configure.rxQuality.set_satype(enums.AddressType.PUBLic)

# CONFigure:BLUetooth:MEAS:RXQuality:GARB ON
cmw_btm.configure.rxQuality.set_garb(True)

# *********************************************************************************
# Execute training phase: Start TX Measurement, return PvT and
# modulation current results, payload length, advertiser address,
# packet and pattern type.
# *********************************************************************************

# Action words like INITIATE, READ, FETCH, ABORt, STARt, STOP are moved from the beginning to the end as method names.
# Action methods always come in pairs: initate() and initiate_with_opc(). Use the initiate_with_opc() for waiting until the measurement is done.
# INITiate:BLUetooth:MEAS:MEValuation
cmw_btm.multiEval.initiate_with_opc()

# FETCh:BLUetooth:MEAS:MEValuation:PVTime:LENergy:LE1M:CURR?
pvt = cmw_btm.multiEval.powerVsTime.lowEnergy.le1M.current.fetch()

# FETCh:BLUetooth:MEAS:MEValuation:MODulation:LENergy:LE1M:CURR?
mod = cmw_btm.multiEval.modulation.lowEnergy.le1M.current.fetch()

# FETCh:BLUetooth:MEAS:ISIGnal:ADETected:PLENgth:LENergy:LE1M?
payload_len = cmw_btm.inputSignal.adetected.plength.lowEnergy.le1M.fetch()

# FETCh:BLUetooth:MEAS:ISIGnal:ADETected:AADDress:LENergy:LE1M?
adv_address = cmw_btm.inputSignal.adetected.aaddress.lowEnergy.le1M.fetch()

# FETCh:BLUetooth:MEAS:ISIGnal:ADETected:PTYPe:LENergy:LE1M?
packet_type = cmw_btm.inputSignal.adetected.ptype.lowEnergy.le1M.fetch()

# FETCh:BLUetooth:MEAS:ISIGnal:ADETected:PATTern:LENergy:LE1M?
pattern_type = cmw_btm.inputSignal.adetected.pattern.lowEnergy.le1M.fetch()

# *********************************************************************************
# Configure Tx-Rx measurement: Select routing for RF output path,
# external attenuation and measurement mode.
# *********************************************************************************

# CONFigure:BLUetooth:MEAS:RXQuality:ROUTe R11,RX11
routing = cmw_btm.configure.rxQuality.route.ValueStruct()
routing.Rx_Connector = enums.RxConnector.R11
routing.Rf_Converter = enums.RxConverter.RX11
cmw_btm.configure.rxQuality.route.set_value(routing)

# CONFigure:BLUetooth:MEAS:RXQuality:ROUTe:USAGe:ALL R118,ON,OFF,OFF,OFF, OFF,OFF,OFF,OFF
cmw_btm.configure.rxQuality.route.usage.all.set(enums.TXConnectorBench, [True, False, False, False, False, False, False, False])

# CONFigure:BLUetooth:MEAS:RXQuality:EATTenuation:OUTPut 5
cmw_btm.configure.rxQuality.eattenuation.set_output(5)
# CONFigure:BLUetooth:MEAS:RXQuality:MMODe SPOT
cmw_btm.configure.rxQuality.set_mmode(enums.RxQualityMeasMode.SPOT)

# *********************************************************************************
# Set spot check Tx level.
# *********************************************************************************

# CONFigure:BLUetooth:MEAS:RXQuality:SPOTcheck:LEVel -40
cmw_btm.configure.rxQuality.spotcheck.set_level(-40)

# *********************************************************************************
# Set  trigger source to Bluetooth Meas:Power.
# *********************************************************************************

# TRIGger:BLUetooth:MEAS:MEValuation:SOURce 'Bluetooth Meas:Power'
cmw_btm.trigger.multiEval.set_source('Bluetooth Meas:Power')

# ******************************************************************************************************************************************************************
# Performing a Tx-Rx Measurement
# ******************************************************************************************************************************************************************

# *********************************************************************************
# Start the measurement and return the contents of the result table.
# Query the measurement state (should be "RDY").
# *********************************************************************************

# INIT:BLUetooth:MEAS:TRX
cmw_btm.trx.initiate_with_opc()

# FETCh:BLUetooth:MEAS:TRX:STATe?
trx_state = cmw_btm.trx.state.fetch()

# FETCh:BLUetooth:MEAS:TRX:STATe:ALL?
trx_state_all = cmw_btm.trx.state.all.fetch()

# *********************************************************************************
# Query all results.
# *********************************************************************************

# FETCh:BLUetooth:MEAS:TRX:ACP?
trx_acp = cmw_btm.trx.acp.fetch()

# FETCh:BLUetooth:MEAS:TRX:MODulation?
trx_mod = cmw_btm.trx.modulation.fetch()

# FETCh:BLUetooth:MEAS:TRX:POWer?
trx_power = cmw_btm.trx.power.fetch()

# FETCh:BLUetooth:MEAS:TRX:SPOT?
trx_spot = cmw_btm.trx.spot.fetch()

cmw_btm.close()
