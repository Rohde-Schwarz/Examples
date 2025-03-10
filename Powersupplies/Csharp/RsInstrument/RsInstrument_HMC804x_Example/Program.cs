using System;
using RohdeSchwarz.RsInstrument; // Nuget Package, install it through the Nuget Package Manager

// Basic C# example for HMC804x - setting of the Voltage and Current, and switching the output ON.
// Please adjust the IP Address to fit your instrument.

namespace MyApp
{
    internal class Program
    {
        static void Main(string[] args)
        {
            var hmc = new RsInstrument("TCPIP::10.102.100.61::INSTR", false, false, "VxiCapable = OFF, AddTermCharToWriteBinData = True");
            Console.WriteLine("Hello, I am " + hmc.Identification.IdnString);
            hmc.Write("INSTrument:Select 1"); // Select channel 1
            hmc.Write("VOLTage 3"); // DC Voltage is 3 V
            hmc.Write("CURRent 1"); // Current set to 1 A
            hmc.Write("OUTPut:CHANnel:STATe 1"); // Set CH1 to active state
            hmc.Write("OUTPut:MASTer:STATe 1"); // Set Main output to active state
            hmc.QueryOpc();
            hmc.Dispose();

            Console.WriteLine("Channel 1: Voltage and Curent set, output is ON.");
            Console.WriteLine("Press any key to finish...");
            Console.ReadKey();
        }
    }
}