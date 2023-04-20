// Basic example on how to work with R&S RsSmcv driver package
// The example does the following:
// - Initializes the session - see the commented lines on how to initialize the session with the specified VISA or no VISA at all
// - Reads the standard information of the instrument
// - Does couple of standard RF settings
// - Shows the standard SCPI write / query communication
// Make sure you:
// - Install the RsSmcv driver package over Packet Manager from Nuget.org
// - Adjust the IP address the match your instrument

using System;
using RohdeSchwarz.RsSmcv;

namespace RsSmcv_Example
{
    class Program
    {
        static void Main()
        {
            var smcv = new RsSmcv("TCPIP::10.102.52.52::HISLIP", true, true);
            //var smcv = new RsSmcv("TCPIP::10.112.1.73::INSTR", true, true, "SelectVisa=RsVisa"); // Forcing R&S VISA
            //var smcv = new RsSmcv("TCPIP::10.112.1.73::5025::SOCKET", true, true, "SelectVisa=SocketIo"); // No VISA needed
            Console.WriteLine("Driver Info: " + smcv.Utilities.Identification.DriverVersion);
            Console.WriteLine($"Selected Visa: {smcv.Utilities.Identification.VisaManufacturer}, DLL: {smcv.Utilities.Identification.VisaDllName}");
            Console.WriteLine("Instrument: " + smcv.Utilities.Identification.IdnString);
            Console.WriteLine("Instrument options: " + string.Join(",", smcv.Utilities.Identification.InstrumentOptions));

            // Driver's instrument status checking ( SYST:ERR? ) after each command (default value is true):
            smcv.Utilities.InstrumentStatusChecking = true;

            // Setting the VISA Timeout to 5000 ms.
            smcv.Utilities.VisaTimeout = 5000;
            
            // Resetting the instrument.
            smcv.Utilities.Reset();

            // Set the output -20 dBm, 223 MHz
            smcv.Output.State.Value = true;
            smcv.Source.Power.Level.Immediate.Amplitude = -20;
            smcv.Source.Frequency.Fixed.Value = 223E6;
            Console.WriteLine($"Channel PEP level: {smcv.Source.Power.Pep:F2} dBm");

            // Direct SCPI interface:
            var response = smcv.Utilities.Query("*IDN?");
            Console.WriteLine($"Direct SCPI response on *IDN?: {response}");

            // Closing the session
            smcv.Dispose();

            Console.Write("\n\nPress any key...");
            Console.ReadKey();
        }
    }
}
