using System;
using RohdeSchwarz.RsOsp;

namespace RsOsp_Example
{
    class Program
    {
        static void Main(string[] args)
        {
            RsOsp osp;
            try // Separate try-catch for initialization prevents accessing uninitialized object
            {
                //-----------------------------------------------------------
                // Initialization:
                //-----------------------------------------------------------
                // Adjust the VISA Resource string to fit your instrument
                osp = new RsOsp("TCPIP::10.212.0.85::INSTR", true, true, "Simulate=0");
                //instr = new RsInstrument("TCPIP::10.112.0.71::5025::SOCKET");
            }
            catch (RohdeSchwarz.RsOsp.RsOspException e)
            {
                Console.WriteLine($"Error initializing the instrument session:\n{e.Message}");
                Console.WriteLine("Press any key to finish.");
                Console.ReadKey();
                return;
            }

            Console.WriteLine($"RsOsp Driver Version: {osp.Utilities.Identification.DriverVersion}");
            Console.WriteLine($"Visa Manufacturer: '{osp.Utilities.Identification.VisaManufacturer}'");
            Console.WriteLine($"Instrument Name: '{osp.Utilities.Identification.InstrumentFullName}'");
            Console.WriteLine($"Instrument Serial Number: '{osp.Utilities.Identification.InstrumentSerialNumber}'");
            Console.WriteLine($"Instrument Firmware: '{osp.Utilities.Identification.InstrumentFirmwareVersion}'");
            Console.WriteLine($"Instrument installed options: '{string.Join(",", osp.Utilities.Identification.InstrumentOptions)}'");

            osp.Route.Path.DeleteAll();
            var pathList = osp.Route.Path.Catalog;
            var pathListCnt = osp.Route.Path.Catalog.Count;
            osp.Route.Path.Define.Set("Test1", "(@F01M01(0201, 0302))");
            pathList = osp.Route.Path.Catalog;
            pathListCnt = osp.Route.Path.Catalog.Count;

            Console.WriteLine("\nPress any key ...");
            Console.ReadKey();

            osp.Dispose();
        }


    }
}
