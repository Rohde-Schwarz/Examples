// Basic example on how to work with R&S RsSgt driver package
// The example does the following:
// - Initializes the session - see the commented lines on how to initialize the session with the specified VISA or no VISA at all
// - Reads the standard information of the instrument
// - Does couple of standard RF settings
// - Shows the standard SCPI write / query communication
// Make sure you:
// - Install the RsSgt driver package over Packet Manager from Nuget.org
// - Adjust the IP address the match your instrument

using System;
using RohdeSchwarz.RsSgt;

namespace RsSgt_Example
{
    class Program
    {
        static void Main()
        {
            var sgt = new RsSgt("TCPIP::10.112.1.73::INSTR", true, true);
            //var sgt = new RsSgt("TCPIP::10.112.1.73::INSTR", true, true, "SelectVisa=RsVisa"); // Forcing R&S VISA
            //var sgt = new RsSgt("TCPIP::10.112.1.73::5025::SOCKET", true, true, "SelectVisa=SocketIo"); // No VISA needed
            Console.WriteLine("Driver Info: " + sgt.Utilities.Identification.DriverVersion);
            Console.WriteLine("Instrument: " + sgt.Utilities.Identification.IdnString);
            Console.WriteLine("Instrument options: " + string.Join(",", sgt.Utilities.Identification.InstrumentOptions));

            // Driver's instrument status checking ( SYST:ERR? ) after each command (default value is true):
            sgt.Utilities.InstrumentStatusChecking = true;
            sgt.Utilities.Reset();

            // Set the output -20 dBm, 223 MHz
            sgt.Output.State.Value = true;
            sgt.Source.Power.Level.Immediate.Amplitude = -20;
            sgt.Source.Frequency.Fixed.Value = 223E6;
            Console.WriteLine($"Channel PEP level: {sgt.Source.Power.Pep:F2} dBm");

            // Direct SCPI interface:
            var response = sgt.Utilities.Query("*IDN?");
            Console.WriteLine($"Direct SCPI response on *IDN?: {response}");

            // Closing the session
            sgt.Dispose();

            Console.Write("\n\nPress any key...");
            Console.ReadKey();
        }
    }
}
