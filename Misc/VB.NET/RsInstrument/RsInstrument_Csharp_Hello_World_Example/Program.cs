// Hello World example for any R&S instrument

#pragma warning disable 219

using System;
using RohdeSchwarz.RsInstrument; // .NET component providing all the necessary VISA extended functionalities. Install as NuGet from www.nuget.org

// Preconditions:
// - R&S VISA 5.12.1+ (or NI VISA 18+)
// - Resource string adjusted to fit your instrument physical connection

// Before starting the program, change the appropriate resource string to fit your instrument interface
// and use it in the RsInstrument() constructor method

namespace RsInstrument_Hello_World_Example
{
    class Program
    {
        static void Main(string[] args)
        {
            RsInstrument instr;
            try // Separate try-catch for initialization prevents accessing uninitialized object
            {
                //-----------------------------------------------------------
                // Initialization:
                //-----------------------------------------------------------
                // Adjust the VISA Resource string to fit your instrument
                var resourceString1 = "TCPIP::10.120.0.110::INSTR"; // Standard LAN connection (also called VXI-11)
                var resourceString2 = "TCPIP::10.120.0.110::hislip0"; // Hi-Speed LAN connection - see 1MA208
                var resourceString3 = "GPIB::20::INSTR"; // GPIB Connection
                var resourceString4 = "USB::0x0AAD::0x0119::022019943::INSTR"; // USB-TMC (Test and Measurement Class)
                var resourceString5 = "RSNRP::0x0095::104015::INSTR"; // R&S Powersensor NRP-Z86

                instr = new RsInstrument( resourceString1 );
            }
            catch (RsInstrumentException e)
            {
                Console.WriteLine($"Error initializing the instrument session:\n{e.Message}");

                Console.Write("\nPress any key ...");
                Console.ReadKey();
                return;
            }

            string idn = instr.QueryString("*IDN?");
            Console.WriteLine($"Hello, I am: '{idn}'");

            Console.WriteLine($"RsInstrument Driver Version: {instr.Identification.DriverVersion}, Core Version: {instr.Identification.CoreVersion}");
            Console.WriteLine($"Visa Manufacturer: '{instr.Identification.VisaManufacturer}'");
            Console.WriteLine($"Instrument Name: '{instr.Identification.InstrumentFullName}'");
            Console.WriteLine($"Instrument installed options: '{string.Join(",", instr.Identification.InstrumentOptions)}'");

            Console.Write("\nPress any key ...");
            Console.ReadKey();

            instr.Dispose();
        }
    }
}