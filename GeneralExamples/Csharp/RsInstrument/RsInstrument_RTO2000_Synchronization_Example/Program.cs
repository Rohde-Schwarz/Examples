// C# example showing the synchronization with the STB polling and WaitForSrq of:
// "SING" command, the program waits for the acquisition to finish
// "*TST?" query, the program waits for the selftest to finish and then reads the result of the selftest
// Use this example for Service Request waiting by changing the RsInstrument object constructor (see below)
// Preconditions:
// - Installed Rohde & Schwarz VISA 5.12.3+ https://www.rohde-schwarz.com/appnote/1dc02 This example will not work without VISA installation

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Threading;
using RohdeSchwarz.RsInstrument; // .NET component providing all the necessary VISA extended functionalities. Install as NuGet from www.nuget.org

namespace RsInstrument_RTO2000_Synchronization_Example
{
    class Program
    {
        static void Main()
        {
            RsInstrument instr;
            RsInstrument.AssertMinVersion("1.18.0");

            try // Separate try-catch for scope initialization prevents accessing uninitialized object
            {
                //-----------------------------------------------------------
                // Initialization:
                //-----------------------------------------------------------
                // Adjust the VISA Resource string to fit your instrument
                // For SRQ waiting, use the following constructor:

                //scope = new RsInstrument("TCPIP::10.212.1.131::INSTR", true, true, "OpcWaitMode=ServiceRequest");
                instr = new RsInstrument("TCPIP::10.212.1.131::INSTR");

                instr.VisaTimeout = 3000; // Timeout for VISA Read Operations
                instr.OpcTimeout = 15000; // Timeout for opc-synchronised operations
                instr.InstrumentStatusChecking = true; // Error check after each command
            }
            catch (RsInstrumentException e)
            {
                Console.WriteLine($"Error initializing the instrument session:\n{e.Message}");
                Console.WriteLine("Press any key to finish.");
                Console.ReadKey();
                return;
            }

            try // try block to catch any InstrumentErrorException() or InstrumentOPCtimeoutException()
            {
                Console.WriteLine($"RsInstrument Driver Version: {instr.Identification.DriverVersion}, Core Version: {instr.Identification.CoreVersion}");
                instr.ClearStatus(); // Clear instrument io buffers
                Console.WriteLine($"Instrument Identification string:\n{instr.Identification.IdnString}");
                instr.WriteString("SYST:DISP:UPD ON"); // Display update switched ON
                //-----------------------------------------------------------
                // Settings all in one string:
                //-----------------------------------------------------------
                instr.WriteString("ACQ:POIN:AUTO RECL;:TIM:RANG 2.0;:ACQ:POIN 1002;:CHAN1:STAT ON;:TRIG1:MODE AUTO");
                //-----------------------------------------------------------
                // Acquisition:
                //-----------------------------------------------------------
                // Sending SCPI command SING and using STB polling synchonization, timeout 6000 ms
                Console.Write("Acquisition started ... ");
                instr.WriteStringWithOpc("SING", 6000);
                Console.WriteLine("finished");
                //-----------------------------------------------------------
                // Selftest:
                //-----------------------------------------------------------
                // Synchronizing of a long-lasting command
                Console.Write("Selftest started ... ");
                instr.QueryStringWithOpc("*TST?", 120000);
                Console.WriteLine("finished");
            }
            catch (RsInstrumentException e)
            {
                Console.WriteLine(e.Message);
            }
            finally
            {
                Console.WriteLine("Press any key to finish...");
                Console.ReadKey();
            }
        }
    }
}
