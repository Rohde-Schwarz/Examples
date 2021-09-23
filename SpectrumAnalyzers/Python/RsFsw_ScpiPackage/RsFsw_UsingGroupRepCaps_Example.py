# Python SCPI package RsFsw example.
# The example shows the default repcap setting done in group objects and / or cloning it.
# Each group can be cloned with clone() method, and then its repcaps can be set independently to other default values.
# These values are then taken as a default for all the methods belonging to that group.
# That means, as long as you do not want to use another repcap value, you can use the method overloads without the repcaps.
# Example (see more in the actual code):
# var tr3 = fsw.Display.Window.Subwindow.Trace.Clone()
# tr3.RepCapTrace = TraceRepCap.Tr3
# Now the following two calls send the same SCPI command: DISPlay1:WINDow:SUBWindow1:TRACe3:MODE MAXHold
# fsw.Display.Window.Subwindow.Trace.Mode.set(TraceModeCenum.MAXHold, WindowRepCap.Nr1, SubWindowRepCap.Nr1, TraceRepCap.Tr3)
# tr3.Mode.set(TraceModeCenum.MAXHold)

# Preconditions:
# - Install the RsFsw driver package over Packet Manager from NuGet.org
# - Adjust the IP address the match your instrument

from RsFsw import *

# A good practice is to check for the installed version
RsFsw.assert_minimum_version('4.90.0')

# Open the session
fsw = RsFsw('TCPIP::192.168.1.102::HISLIP', reset=True)
# Greetings, stranger...
print(f'Hello, I am: {fsw.utilities.idn_string}')

fsw = RsFsw("TCPIP::localhost::HISLIP", True, True)
# fsw = RsFsw("TCPIP::localhost::HISLIP", True, True, options='SelectVisa=RsVisa')  # Forcing R&S VISA
# fsw = RsFsw("TCPIP::localhost::5025::SOCKET", True, True, options='SelectVisa=SocketIo')  # No VISA installation needed

# Driver's instrument status checking ( SYST:ERR? ) after each command (default value is true):
fsw.utilities.instrument_status_checking = True

#   SYSTem:DISPlay:UPDate ON
fsw.system.display.update.set(True)

#   INITiate:CONTinuous OFF
fsw.initiate.continuous.set(True)
print('Always work in single-sweep mode.')

#   SENSe.FREQuency:STARt 100000000
fsw.sense.frequency.start.set(100E6)

#   SENSe.FREQuency:STOP 200000000
fsw.sense.frequency.stop.set(200E6)

#   DISPlay:WINDow:TRACe:Y:SCALe:RLEVel -20.0
fsw.display.window.trace.y.scale.refLevel.set(-20.0)

#   DISPlay:WINDow:SUBWindow:TRACe:Y:SCALe 60.0
fsw.display.window.subwindow.trace.y.scale.set(60.0)

# Prepare tr1 and tr2 to work with the trace 1 and trace 2 interfaces:
tr1 = fsw.display.window.subwindow.trace.clone()
tr1.repcap_trace_set(repcap.Trace.Tr1)
tr2 = fsw.display.window.subwindow.trace.clone()
tr2.repcap_trace_set(repcap.Trace.Tr2)

# Standard usage with all the repcaps defined in the method call:
#   DISPlay1:WINDow:SUBWindow:TRACe1:MODE MAXHold
fsw.display.window.subwindow.trace.mode.set(enums.TraceModeC.MAXHold, repcap.Window.Nr1, repcap.SubWindow.Nr1, repcap.Trace.Tr1)
# Now the following call sends the same command:
tr1.mode.set(enums.TraceModeC.MAXHold)

#   DISPlay1:WINDow:SUBWindow:TRACe2:MODE MINHold
fsw.display.window.subwindow.trace.mode.set(enums.TraceModeC.MINHold, repcap.Window.Nr1, repcap.SubWindow.Nr1, repcap.Trace.Tr2)
# Now the following call sends the same command:
tr2.mode.set(enums.TraceModeC.MINHold)

#   SENSe:SWEep:POINts 10001
fsw.sense.sweep.points.set(10001)

#   INITiate:IMMediate (set timeout 3000 ms)
fsw.initiate.immediate_with_opc(3000)

#            TRACe1:DATA?
trace1 = fsw.trace.data.get(enums.TraceNumber.TRACe1)

#            TRACe2:DATA?
trace2 = fsw.trace.data.get(enums.TraceNumber.TRACe2)

#   CALCulate1:MARKer1:TRACe 1
fsw.calculate.marker.trace.set(1, repcap.Window.Nr1, repcap.Marker.Nr1)
mark1 = fsw.calculate.marker.clone()
mark1.RepCapMarker = repcap.Marker.Nr1

#   CALCulate1:MARKer1:MAXimum:PEAK
fsw.calculate.marker.maximum.peak.set(repcap.Window.Nr1, repcap.Marker.Nr1)
# Same command with the mark1 interface:
mark1.maximum.peak.set()

#         CALCulate1:MARKer1:X?
m1x = fsw.calculate.marker.x.get(repcap.Window.Nr1, repcap.Marker.Nr1)
# Same command with the mark1 interface:
m1x = mark1.x.get()

#         CALCulate1:MARKer1:Y?
m1y = fsw.calculate.marker.y.get(repcap.Window.Nr1, repcap.Marker.Nr1)
# Same command with the mark1 interface:
m1y = mark1.y.get()

print(f'Trace 1 points: {len(trace1)}')
print(f'Trace 1 Marker 1: {m1x} Hz, {m1y} dBm')

#   CALCulate1:MARKer2:TRACe 2
fsw.calculate.marker.trace.set(2, repcap.Window.Nr1, repcap.Marker.Nr2)
mark2 = fsw.calculate.marker.clone()
mark2.RepCapMarker = repcap.Marker.Nr2

#   CALCulate1:MARKer2:MINimum:PEAK
fsw.calculate.marker.minimum.peak.set(repcap.Window.Nr1, repcap.Marker.Nr2)
# Same effect with the mark2 interface:
mark2.minimum.peak.set()

#         CALCulate2:MARKer2:X?
m2x = fsw.calculate.marker.x.get(repcap.Window.Nr1, repcap.Marker.Nr2)
# Same effect with the mark1 interface:
m2x = mark2.x.get()

#         CALCulate2:MARKer2:Y?
m2y = fsw.calculate.marker.y.get(repcap.Window.Nr1, repcap.Marker.Nr2)
# Same command with the mark1 interface:
m2y = mark2.y.get()

print(f'Trace 2 points: {len(trace2)}')
print(f'Trace 2 Marker 2: {m2x} Hz, {m2y} dBm')

# Close the session
fsw.close()
