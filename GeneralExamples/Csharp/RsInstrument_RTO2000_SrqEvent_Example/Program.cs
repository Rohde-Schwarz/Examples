// C# example showing the synchronization of the "SING" command with the Service Request event handler
// Event handler Scope_SrqHandler() is called when the instrument generates Service Request.
// Preconditions:
// - Installed Rohde & Schwarz VISA 5.12.3+ https://www.rohde-schwarz.com/appnote/1dc02 This example will not work without VISA installation

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Threading;
using RohdeSchwarz.RsInstrument; // .NET component providing all the necessary VISA extended functionalities. Install as NuGet from www.nuget.org

namespace Csharp_VISA.NET_Scope_SRQevent_Example
{
    class Program
    {
        // Event handler for our Service Request Event
        private static void Scope_SrqHandler(object sender, InstrEventArgs e)
        {
            Console.WriteLine("-----------------------------------");
            Console.WriteLine("Service Request Event generated");
            Console.WriteLine("-----------------------------------");
        }
        static void Main()
        {

            RsInstrument instr;
            RsInstrument.AssertMinVersion("1.8.0");

            try // Separate try-catch for scope initialization prevents accessing uninitialized object
            {
                //-----------------------------------------------------------
                // Initialization:
                //-----------------------------------------------------------
                // Adjust the VISA Resource string to fit your instrument
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

            try // try block to catch any InstrumentErrorException()
            {
                Console.WriteLine($"RsInstrument Driver Version: {instr.Identification.DriverVersion}, Core Version: {instr.Identification.CoreVersion}");
                instr.ClearStatus(); // Clear instrument status - errors and io buffers
                Console.WriteLine($"Instrument Identification string:\n{instr.Identification.IdnString}");
                instr.WriteString("*RST;*CLS"); // Reset the instrument, clear the Error queue
                instr.WriteString("SYST:DISP:UPD ON"); // Display update ON - switch OFF after debugging
                //-----------------------------------------------------------
                // Basic Settings:
                //-----------------------------------------------------------
                instr.WriteString("ACQ:POIN:AUTO RECL;:TIM:RANG 2.0;:ACQ:POIN 1002;:CHAN1:STAT ON;:TRIG1:MODE AUTO"); // Define Horizontal scale by number of points
                //-----------------------------------------------------------
                // Acquisitions:
                //-----------------------------------------------------------
                Console.WriteLine("Acquisition no. 1 started...");
                instr.Events.WriteWithOpcHandler = Scope_SrqHandler;
                instr.Events.WriteStringWithOpc("SING"); // Send the SING command and call Scope_SrqHandler() when finished.
                Thread.Sleep(6000); // Wait here for invoking the handler Scope_SrqHandler()

                // Repeat
                Console.WriteLine("Acquisition no. 2 started...");
                instr.Events.WriteStringWithOpc("SING"); // Send the SING command and call Scope_SrqHandler() when finished.
                Thread.Sleep(6000); // Wait here for invoking the handler Scope_ServiceRequest()
                instr.Events.WriteWithOpcHandler = null; // remove the handler
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
