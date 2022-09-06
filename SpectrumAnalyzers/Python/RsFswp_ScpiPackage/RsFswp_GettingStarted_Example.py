"""Getting started - how to work with RsFswp Python SCPI package.
This example performs basic RF settings and measurements on an FSW instrument.
It shows the RsFswp calls and their corresponding SCPI commands.
Notice that the python RsFswp interfaces track the SCPI commands syntax."""

from RsFswp import *

# A good practice is to check for the installed version
RsFswp.assert_minimum_version('2.0.0')

# Open the session
fswp = RsFswp('TCPIP::localhost::HISLIP', reset=True)
# Greetings, stranger...
print(f'Hello, I am: {fswp.utilities.idn_string}')

# Print commands to the console with the logger
fswp.utilities.logger.mode = LoggingMode.On
fswp.utilities.logger.log_to_console = True

# Driver's instrument status checking ( SYST:ERR? ) after each command (default value is true):
fswp.utilities.instrument_status_checking = True

#   SYSTem:DISPlay:UPDate ON
fswp.system.display.update.set(True)

#   INITiate:CONTinuous OFF
fswp.initiate.continuous.set(False)
print(f'Always work in single-sweep mode.')

#   SENSe.FREQuency:STARt 100000000
fswp.sense.frequency.start.set(100E6)

#   SENSe.FREQuency:STOP 200000000
fswp.sense.frequency.stop.set(200E6)

#   DISPlay:WINDow:TRACe:Y:SCALe:RLEVel -20.0
fswp.display.window.trace.y.scale.refLevel.set(-20.0)

#   DISPlay1:WINDow:SUBWindow:TRACe1:MODE:MAXHold
fswp.display.window.subwindow.trace.mode.set(enums.TraceModeC.MAXHold, repcap.Window.Nr1, repcap.SubWindow.Default, repcap.Trace.Tr1)

#   DISPlay1: WINDow:SUBWindow:TRACe2:MODE MINHold
fswp.display.window.subwindow.trace.mode.set(enums.TraceModeC.MINHold, repcap.Window.Nr1, repcap.SubWindow.Default, repcap.Trace.Tr2)

#   SENSe:SWEep:POINts 10001
fswp.sense.sweep.points.set(10001)

#    INITiate:IMMediate (with timeout 3000 ms)
fswp.initiate.immediate_with_opc(3000)

#            TRACe1:DATA?
trace1 = fswp.trace.data.get(enums.TraceNumber.TRACe1)

#            TRACe2:DATA?
trace2 = fswp.trace.data.get(enums.TraceNumber.TRACe2)

#   CALCulate1:MARKer1:TRACe 1
fswp.calculate.marker.trace.set(1, repcap.Window.Nr1, repcap.Marker.Nr1)

#   CALCulate1:MARKer1:MAXimum:PEAK
fswp.calculate.marker.maximum.peak.set(repcap.Window.Nr1, repcap.Marker.Nr1)
#         CALCulate1:MARKer1:X?
m1x = fswp.calculate.marker.x.get(repcap.Window.Nr1, repcap.Marker.Nr1)

#         CALCulate1:MARKer1:Y?
m1y = fswp.calculate.marker.y.get(repcap.Window.Nr1, repcap.Marker.Nr1)

print(f'Trace 1 points: {len(trace1)}')
print(f'Trace 1 Marker 1: {m1x} Hz, {m1y} dBm')

#   CALCulate1:MARKer2:TRACe 2
fswp.calculate.marker.trace.set(2, repcap.Window.Nr1, repcap.Marker.Nr2)

#   CALCulate1:MARKer2:MINimum:PEAK
fswp.calculate.marker.minimum.peak.set(repcap.Window.Nr1, repcap.Marker.Nr2)

#         CALCulate2:MARKer2:X?
m2x = fswp.calculate.marker.x.get(repcap.Window.Nr1, repcap.Marker.Nr2)

#         CALCulate2:MARKer2:Y?
m2y = fswp.calculate.marker.y.get(repcap.Window.Nr1, repcap.Marker.Nr2)

print(f'Trace 1 points: {len(trace2)}')
print(f'Trace 1 Marker 1: {m2x} Hz, {m2y} dBm')

# Close the session
fswp.close()
