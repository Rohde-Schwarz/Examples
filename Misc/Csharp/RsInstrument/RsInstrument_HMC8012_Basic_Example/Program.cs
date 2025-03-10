using System;
using RohdeSchwarz.RsInstrument; // Nuget Package, install it through the Nuget Package Manager

// Basic C# example for HMC8012 - setting of the DC Voltage measurement, and reading one value.
// Please adjust the IP Address to fit your instrument.

namespace MyApp
{
    internal class Program
    {
        static void Main(string[] args)
        {
            var hmc = new RsInstrument("TCPIP::10.102.100.49::INSTR", false, false, "VxiCapable = OFF, AddTermCharToWriteBinData = True");
            Console.WriteLine("Hello, I am " + hmc.Identification.IdnString);
            hmc.Write("CONF:VOLT:DC AUTO,0.01"); // DC Voltage measurement.
            var meas = hmc.Query("READ?"); // Read the result
            Console.WriteLine($"Measured DC Voltage: {meas} V");
            hmc.Dispose();

            Console.WriteLine("Press any key to finish...");
            Console.ReadKey();
        }
    }
}