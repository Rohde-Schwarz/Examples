// This RsFsw C# SCPI package example shows creating new FSW applications and arranging windows

// Preconditions:
// - Install the RsFsw driver package over Packet Manager from NuGet.org
// - Adjust the IP address the match your instrument

using System;
using RohdeSchwarz.RsFsw;

namespace RsFsw_ArrangingWindows_Example
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

            //  Update display in remote
            fsw.System.Display.Update.Set(true);

            // Create new instrument 'VSA'
            fsw.Instrument.Create.New.Set(ChannelTypeEnum.K70_VectorSignalAnalyzer, "MyVsa");
            // Create new instrument 'Pulse'
            fsw.Instrument.Create.New.Set(ChannelTypeEnum.K6_PulseAnalysis, "MyPulse");

            // Select the specan instrument by instrument name
            fsw.Instrument.Select.Set(ChannelTypeEnum.SpectrumAnalyzer);

            // Select the MyVsa by name
            fsw.Instrument.SelectName.Set("MyVsa");

            var channels = fsw.Instrument.List.Get();
            Console.WriteLine("All active channels (type, name):" + string.Join(", ", channels));

            // Get catalog of all the active windows in the VSA
            var windows = fsw.Layout.Catalog.Window.Get();
            Console.WriteLine("All active windows in the VSA (number, name):" + string.Join(", ", channels));

            // Add new window with EVM results to the right of the ResultSummary window
            var newName = fsw.Applications.K70_Vsa.Layout.Add.Window.Get("2", WindowDirectionEnum.RIGHt, WindowTypeK70enum.ErrorVectorMagnitude);
            Console.WriteLine($"Newly created window name: '{newName}'");
            // Now move the window '1' to the right from the newly created window:
            fsw.Applications.K70_Vsa.Layout.Move.Window.Set("1", newName, WindowDirReplaceEnum.RIGHt);

            // Close the session
            fsw.Dispose();

            Console.WriteLine("\nPress any key");
            Console.ReadKey();
        }
    }
}
