// Hello World example for any R&S instrument

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using RohdeSchwarz.RsInstrument; // .NET component providing all the necessary VISA extended functionalities. Install as NuGet from www.nuget.org

namespace RsInstrument_Hello_World_Example
{
    class Program
    {
        static void Main()
        {
            RsInstrument instr;
            RsInstrument.AssertMinVersion("1.6.0");

            try // Separate try-catch for initialization prevents accessing uninitialized object
            {
                //-----------------------------------------------------------
                // Initialization:
                //-----------------------------------------------------------
                // Adjust the VISA Resource string to fit your instrument
                instr = new RsInstrument("TCPIP::10.112.1.116::INSTR");
                //instr = new RsInstrument("TCPIP::10.112.1.140::5025::SOCKET");
            }
            catch (RsInstrumentException e)
            {
                Console.WriteLine($"Error initializing the instrument session:\n{e.Message}");
                Console.WriteLine("Press any key to finish.");
                Console.ReadKey();
                return;
            }

            Console.WriteLine($"RsInstrument Driver Version: {instr.Identification.DriverVersion}, Core Version: {instr.Identification.CoreVersion}");
            Console.WriteLine($"Visa Manufacturer: '{instr.Identification.VisaManufacturer}'");
            Console.WriteLine($"Instrument Name: '{instr.Identification.InstrumentFullName}'");
            Console.WriteLine($"Instrument installed options: '{string.Join(",", instr.Identification.InstrumentOptions)}'");
            string idn = instr.QueryString("*IDN?");
            Console.WriteLine($"Hello, I am: '{idn}'");

            Console.WriteLine("\nPress any key to finish ...");
            Console.ReadKey();
            
            instr.Dispose();
        }
    }
}