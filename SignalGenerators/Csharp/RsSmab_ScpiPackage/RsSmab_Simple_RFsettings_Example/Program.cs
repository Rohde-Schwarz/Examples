// Basic example on how to work with R&S RsSmab driver package
// The example does the following:
// - Initializes the session - see the commented lines on how to initialize the session with the specified VISA or no VISA at all
// - Reads the standard information of the instrument
// - Does couple of standard RF settings
// - Shows the standard SCPI write / query communication
// Make sure you:
// - Install the RsSmab driver package over Packet Manager from Nuget.org
// - Adjust the IP address the match your instrument

using System;
using RohdeSchwarz.RsSmab;

namespace RsSmab_Example
{
    class Program
    {
        static void Main()
        {
            var smab = new RsSmab("TCPIP::10.112.1.64::INSTR", true, true);
            //var smab = new RsSmab("TCPIP::10.112.1.73::INSTR", true, true, "SelectVisa=RsVisa"); // Forcing R&S VISA
            //var smab = new RsSmab("TCPIP::10.112.1.73::5025::SOCKET", true, true, "SelectVisa=SocketIo"); // No VISA needed
            Console.WriteLine("Driver Info: " + smab.Utilities.Identification.DriverVersion);
            Console.WriteLine($"Selected Visa: {smab.Utilities.Identification.VisaManufacturer}, DLL: {smab.Utilities.Identification.VisaDllName}");
            Console.WriteLine("Instrument: " + smab.Utilities.Identification.IdnString);
            Console.WriteLine("Instrument options: " + string.Join(",", smab.Utilities.Identification.InstrumentOptions));

            // Driver's instrument status checking ( SYST:ERR? ) after each command (default value is true):
            smab.Utilities.InstrumentStatusChecking = true;
            smab.Utilities.Reset();

            // Set the output -21.3 dBm, 224 MHz
            smab.Output.State.Value = true;
            smab.Source.Power.Level.Immediate.Amplitude = -21.3;
            smab.Source.Frequency.Fixed.Value = 234E6;

            // Direct SCPI interface:
            var response = smab.Utilities.QueryString("*IDN?");
            Console.WriteLine($"Direct SCPI response on *IDN?: {response}");

            // Closing the session
            smab.Dispose();

            Console.Write("\n\nPress any key...");
            Console.ReadKey();
        }
    }
}
