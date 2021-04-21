// Basic example on how to work with R&S RsSmbv driver package
// The example does the following:
// - Initializes the session - see the commented lines on how to initialize the session with the specified VISA or no VISA at all
// - Reads the standard information of the instrument
// - Does couple of standard RF settings
// - Shows the standard SCPI write / query communication
// Make sure you:
// - Install the RsSmbv driver package over Packet Manager from Nuget.org
// - Adjust the IP address the match your instrument

using System;
using RohdeSchwarz.RsSmbv;

namespace RsSmbv_Example
{
    class Program
    {
        static void Main()
        {
            var smbv = new RsSmbv("TCPIP::10.112.1.73::INSTR", true, true);
            //var smbv = new RsSmbv("TCPIP::10.112.1.73::INSTR", true, true, "SelectVisa=RsVisa"); // Forcing R&S VISA
            //var smbv = new RsSmbv("TCPIP::10.112.1.73::5025::SOCKET", true, true, "SelectVisa=SocketIo"); // No VISA needed
            Console.WriteLine("Driver Info: " + smbv.Utilities.Identification.DriverVersion);
            Console.WriteLine($"Selected Visa: {smbv.Utilities.Identification.VisaManufacturer}, DLL: {smbv.Utilities.Identification.VisaDllName}");
            Console.WriteLine("Instrument: " + smbv.Utilities.Identification.IdnString);
            Console.WriteLine("Instrument options: " + string.Join(",", smbv.Utilities.Identification.InstrumentOptions));

            // Driver's instrument status checking ( SYST:ERR? ) after each command (default value is true):
            smbv.Utilities.InstrumentStatusChecking = true;
            smbv.Utilities.Reset();

            // Set the output -20 dBm, 223 MHz
            smbv.Output.State.Value = true;
            smbv.Source.Power.Level.Immediate.Amplitude = -20;
            smbv.Source.Frequency.Fixed.Value = 223E6;
            Console.WriteLine($"Channel PEP level: {smbv.Source.Power.Pep:F2} dBm");

            // Direct SCPI interface:
            var response = smbv.Utilities.QueryString("*IDN?");
            Console.WriteLine($"Direct SCPI response on *IDN?: {response}");

            // Closing the session
            smbv.Dispose();

            Console.Write("\n\nPress any key...");
            Console.ReadKey();
        }
    }
}
