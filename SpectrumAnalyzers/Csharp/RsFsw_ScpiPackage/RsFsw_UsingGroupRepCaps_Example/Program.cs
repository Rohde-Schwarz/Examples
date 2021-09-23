// C# SCPI package RsFsw example.
// The example shows the default repcap setting done in group objects and / or cloning it.
// Each group can be cloned with Clone() method, and then its repcaps can be set independently to other default values.
// These values are then taken as a default for all the methods belonging to that group.
// That means, as long as you do not want to use another repcap value, you can use the method overloads without the repcaps.
// Example (see more in the actual code):
// var tr3 = fsw.Display.Window.Subwindow.Trace.Clone();
// tr3.RepCapTrace = TraceRepCap.Tr3;
// Now the following two calls send the same SCPI command: DISPlay1:WINDow:SUBWindow1:TRACe3:MODE MAXHold
// fsw.Display.Window.Subwindow.Trace.Mode.Set(TraceModeCenum.MAXHold, WindowRepCap.Nr1, SubWindowRepCap.Nr1, TraceRepCap.Tr3);
// tr3.Mode.Set(TraceModeCenum.MAXHold);

// Preconditions:
// - Install the RsFsw driver package over Packet Manager from NuGet.org
// - Adjust the IP address the match your instrument

using System;
using RohdeSchwarz.RsFsw;

namespace RsFsw_UsingGroupRepCaps_Example
{
    class Program
    {
        static void Main(string[] args)
        {
            var fsw = new RsFsw("TCPIP::192.168.1.102::HISLIP", true, true);
            //var fsw = new RsFsw("TCPIP::192.168.1.102::INSTR", true, true, "SelectVisa=RsVisa"); // Forcing R&S VISA
            //var fsw = new RsFsw("TCPIP::192.168.1.102::5025::SOCKET", true, true, "SelectVisa=SocketIo"); // No VISA installation needed
            Console.WriteLine("Instrument: " + fsw.Utilities.Identification.IdnString);

            // Driver's instrument status checking ( SYST:ERR? ) after each command (default value is true):
            fsw.Utilities.InstrumentStatusChecking = true;

            //  SYSTem:DISPlay:UPDate ON
            fsw.System.Display.Update.Set(true);

            //  INITiate:CONTinuous OFF
            fsw.Initiate.Continuous.Set(false);
            Console.WriteLine("Always work in single-sweep mode.");

            //  SENSe.FREQuency:STARt 100000000
            fsw.Sense.Frequency.Start.Set(100E6);

            //  SENSe.FREQuency:STOP 200000000
            fsw.Sense.Frequency.Stop.Set(200E6);

            //  DISPlay:WINDow:TRACe:Y:SCALe:RLEVel -20.0
            fsw.Display.Window.Trace.Y.Scale.RefLevel.Set(-20.0);

            //  DISPlay:WINDow:SUBWindow:TRACe:Y:SCALe 60.0
            fsw.Display.Window.Subwindow.Trace.Y.Scale.Set(60.0);

            // Prepare tr1 and tr2 to work with the trace 1 and trace 2 interfaces:
            var tr1 = fsw.Display.Window.Subwindow.Trace.Clone();
            tr1.RepCapTrace = TraceRepCap.Tr1;
            var tr2 = fsw.Display.Window.Subwindow.Trace.Clone();
            tr2.RepCapTrace = TraceRepCap.Tr2;

            // Standard usage with all the repcaps defined in the method call:
            //  DISPlay1:WINDow:SUBWindow:TRACe1:MODE MAXHold
            fsw.Display.Window.Subwindow.Trace.Mode.Set(TraceModeCenum.MAXHold, WindowRepCap.Nr1, SubWindowRepCap.Nr1, TraceRepCap.Tr1);
            // Now the following call sends the same command:
            tr1.Mode.Set(TraceModeCenum.MAXHold);

            //  DISPlay1:WINDow:SUBWindow:TRACe2:MODE MINHold
            fsw.Display.Window.Subwindow.Trace.Mode.Set(TraceModeCenum.MINHold, WindowRepCap.Nr1, SubWindowRepCap.Nr1, TraceRepCap.Tr2);
            // Now the following call sends the same command:
            tr2.Mode.Set(TraceModeCenum.MINHold);

            //  SENSe:SWEep:POINts 10001
            fsw.Sense.Sweep.Points.Set(10001);

            //   INITiate:IMMediate (with timeout 3000 ms)
            fsw.Initiate.ImmediateAndWait(3000);

            //               TRACe1:DATA?
            var trace1 = fsw.Trace.Data.Get(TraceNumberEnum.TRACe1);

            //               TRACe2:DATA?
            var trace2 = fsw.Trace.Data.Get(TraceNumberEnum.TRACe2);

            //  CALCulate1:MARKer1:TRACe 1
            fsw.Calculate.Marker.Trace.Set(1, WindowRepCap.Nr1, MarkerRepCap.Nr1);
            var mark1 = fsw.Calculate.Marker.Clone();
            mark1.RepCapMarker = MarkerRepCap.Nr1;

            // CALCulate1:MARKer1:MAXimum:PEAK
            fsw.Calculate.Marker.Maximum.Peak.Set(WindowRepCap.Nr1, MarkerRepCap.Nr1);
            // Same command with the mark1 interface:
            mark1.Maximum.Peak.Set();

            //            CALCulate1:MARKer1:X?
            var m1x = fsw.Calculate.Marker.X.Get(WindowRepCap.Nr1, MarkerRepCap.Nr1);
            // Same command with the mark1 interface:
            m1x = mark1.X.Get();

            //            CALCulate1:MARKer1:Y?
            var m1y = fsw.Calculate.Marker.Y.Get(WindowRepCap.Nr1, MarkerRepCap.Nr1);
            // Same command with the mark1 interface:
            m1y = mark1.Y.Get();

            Console.WriteLine($"Trace 1 points: {trace1.Count}");
            Console.WriteLine($"Trace 1 Marker 1: {m1x} Hz, {m1y:F2} dBm");

            //  CALCulate1:MARKer2:TRACe 2
            fsw.Calculate.Marker.Trace.Set(2, WindowRepCap.Nr1, MarkerRepCap.Nr2);
            var mark2 = fsw.Calculate.Marker.Clone();
            mark2.RepCapMarker = MarkerRepCap.Nr2;

            //  CALCulate1:MARKer2:MINimum:PEAK
            fsw.Calculate.Marker.Minimum.Peak.Set(WindowRepCap.Nr1, MarkerRepCap.Nr2);
            // Same effect with the mark2 interface:
            mark2.Maximum.Peak.Set();

            //            CALCulate2:MARKer2:X?
            var m2x = fsw.Calculate.Marker.X.Get(WindowRepCap.Nr1, MarkerRepCap.Nr2);
            // Same effect with the mark1 interface:
            m2x = mark2.X.Get();

            //            CALCulate2:MARKer2:Y?
            var m2y = fsw.Calculate.Marker.Y.Get(WindowRepCap.Nr1, MarkerRepCap.Nr2);
            // Same command with the mark1 interface:
            m2y = mark2.Y.Get();

            Console.WriteLine($"Trace 2 points: {trace2.Count}");
            Console.WriteLine($"Trace 2 Marker 2: {m2x} Hz, {m2y:F2} dBm");

            // Close the session
            fsw.Dispose();

            Console.WriteLine("\nPress any key");
            Console.ReadKey();
        }
    }
}
