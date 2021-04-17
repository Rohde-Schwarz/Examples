// Hello World example for any R&S instrument
// - Preconditions: 
// - Installed Rohde & Schwarz VISA 5.12.3+ https://www.rohde-schwarz.com/appnote/1dc02
// - You can also work without VISA - see the 'Initialization' section 

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
            RsInstrument.AssertMinVersion("1.10.1");

            try // Separate try-catch for initialization prevents accessing uninitialized object
            {
                //-----------------------------------------------------------
                // Initialization:
                //-----------------------------------------------------------
                // Adjust the VISA Resource string to fit your instrument
                instr = new RsInstrument("TCPIP::10.112.1.67::INSTR");
                
                // For socket instrument, use the following:
                // instr = new RsInstrument("TCPIP::10.112.1.140::5025::SOCKET");
                
                // If you want to avoid VISA installation:
                // instr = new RsInstrument("TCPIP::10.112.1.179::5025::SOCKET", false, false, "SelectVisa=SocketIO");
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