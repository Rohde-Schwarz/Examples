using System;
using RohdeSchwarz.RsInstrument; // RsInstrument is a Nuget Package, install it through the Nuget Package Manager

/* Example for remote-controlling R&S Vector Network Analyzers.
 It shows the following:
 - Sets up Channel 1 and one Trace to Input Impedance measurement
 - Sets 200 impedance points between 10MHz and 2GHz
 - Performs a single sweep
 - Reads out the impedance sweep data to the PC
*/

namespace RsInstrument_Vna_TDR_LP_Step_Impedance_Example
{
    class Program
    {
        static void Main()
        {
            RsInstrument vna;
            try //separate try-catch for initialization prevents accessing uninitialized object
            {
                //-----------------------------------------------------------
                //Initialization:
                //-----------------------------------------------------------
                // Adjust the VISA Resource string to fit your instrument
                vna = new RsInstrument("TCPIP::192.168.1.100:hislip0", true, true);
                Console.WriteLine($"Instrument Identification string: \n{vna.Identification.IdnString}");
            }
            catch (RsInstrumentException e)
            {
                Console.WriteLine("Error initializing the instrument session:\n{0}", e.Message);
                Console.WriteLine("Press any key to finish.");
                Console.ReadKey();
                return;
            }

            // Preset instrument
            vna.Reset();

            // Configure channel with harmonic grid
            vna.Write("SENS1:FREQ:STAR 10.0 MHz");
            vna.Write("SENS1:FREQ:STOP 2.0 GHz");
            vna.Write("SENS1:SWE:POIN 200");
            vna.Write("SENS1:BAND 5 KHz");
            vna.Write("SOUR1:POW -5 dBm");
            
            // Trace: Z->S11
            vna.Write("CALC1:PAR:SDEF 'Trc1', 'Z-S11'");
            vna.Write("DISP:WIND1:STAT ON");
            vna.Write("DISP:WIND1:TRAC:EFE 'Trc1'");
            vna.Write("CALC1:FORM REAL");
            
            // Time domain 0-99 ns, lowpass step
            vna.Write("CALC1:TRAN:TIME:STAR 0 ns");
            vna.Write("CALC1:TRAN:TIME:STOP 99 ns");
            vna.Write("CALC1:TRAN:TIME:TYPE LPAS");
            vna.Write("CALC1:TRAN:TIME:STIM STEP");
            vna.Write("CALC1:TRAN:TIME:WIND HANN");
            vna.Write("CALC1:TRAN:TIME:LPAS:DCSP:CONT ON");
            vna.Write("CALC1:TRAN:TIME:STAT ON");
            
            // Scale 0-200 Ohms
            vna.Write("DISP:WIND:TRAC:Y:PDIV 20, 'Trc1'");
            vna.Write("DISP:WIND:TRAC:Y:RPOS 0, 'Trc1'");
            vna.Write("DISP:WIND:TRAC:Y:RLEV 0, 'Trc1'");

            // Only when all the settings are complete, continue further
            vna.QueryOpc();

            // Perform one single sweep
            vna.Write("INIT:CONT:ALL OFF");
            Console.Write("\nStarting the sweep... ");
            vna.Write("INIT:ALL");
            // Wait for the sweep to finish before continuing further
            vna.QueryOpc();
            Console.WriteLine("finished\n");

            // Query the data to the PC
            var impedanceTrace = vna.Binary.QueryBinOrAsciiFloatArray("FORMat:DATA REAL,32;:CALC1:DATA? FDAT");
            Console.WriteLine($"Queried {impedanceTrace.Length} impedance data points");

            // Close the session
            vna.Dispose();

            Console.WriteLine("\nPress any key to finish.");
            Console.ReadKey();
        }
    }
}
