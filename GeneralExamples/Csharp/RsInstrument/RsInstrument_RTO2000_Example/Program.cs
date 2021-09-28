// C# Example for RTO / RTE / RTP Oscilloscopes
// Preconditions:
// - Installed Rohde & Schwarz VISA 5.12.3+ https://www.rohde-schwarz.com/appnote/1dc02
// - You can also work without VISA by using LAN SocketIO - see Hello_World example

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using RohdeSchwarz.RsInstrument; // .NET component providing all the necessary VISA extended functionalities. Install as NuGet from www.nuget.org

namespace RsInstrument_RTO2000_Example
{
    class Program
    {
        static void Main()
        {
            RsInstrument instr;
            RsInstrument.AssertMinVersion("1.13.0");

            try // Separate try-catch for initialization prevents accessing uninitialized object
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
                instr.ClearStatus(); //Clear instrument status - errors and io buffers
                Console.WriteLine($"Instrument Identification string:\n{instr.Identification.IdnString}");
                instr.WriteString("*RST;*CLS"); // Reset the instrument, clear the Error queue
                instr.WriteString("SYST:DISP:UPD ON"); // Display update ON - switch OFF after debugging
                //-----------------------------------------------------------
                // Basic Settings:
                //-----------------------------------------------------------
                instr.WriteString("ACQ:POIN:AUTO RECL"); // Define Horizontal scale by number of points
                instr.WriteString("TIM:RANG 0.01"); // 10ms Acquisition time
                instr.WriteString("ACQ:POIN 20002"); // 20002 X points
                instr.WriteString("CHAN1:RANG 2"); // Horizontal range 2V
                instr.WriteString("CHAN1:POS 0"); // Offset 0
                instr.WriteString("CHAN1:COUP AC"); // Coupling AC 1MOhm
                instr.WriteString("CHAN1:STAT ON"); // Switch Channel 1 ON
                //-----------------------------------------------------------
                // Trigger Settings:
                //-----------------------------------------------------------
                instr.WriteString("TRIG1:MODE AUTO"); // Trigger Auto mode in case of no signal is applied
                instr.WriteString("TRIG1:SOUR CHAN1"); // Trigger source CH1
                instr.WriteString("TRIG1:TYPE EDGE;:TRIG1:EDGE:SLOP POS"); // Trigger type Edge Positive
                instr.WriteString("TRIG1:LEV1 0.04"); // Trigger level 40mV
                instr.QueryOpc(); // Using *OPC? query waits until all the instrument settings are finished
                // -----------------------------------------------------------
                // SyncPoint 'SettingsApplied' - all the settings were applied
                // -----------------------------------------------------------
                // Arming the SCOPE for single acquisition
                // -----------------------------------------------------------
                instr.VisaTimeout = 2000; // Acquisition timeout - set it higher than the acquisition time
                instr.WriteString("SING");
                // -----------------------------------------------------------
                // DUT_Generate_Signal() - in our case we use Probe compensation signal
                // where the trigger event (positive edge) is reoccuring
                // -----------------------------------------------------------
                instr.QueryOpc(); // Using *OPC? query waits until the instrument finished the Acquisition
                // -----------------------------------------------------------
                // SyncPoint 'AcquisitionFinished' - the results are ready
                // -----------------------------------------------------------
                // Fetching the waveform in ASCII format
                // -----------------------------------------------------------
                double[] waveformAsc = instr.Binary.QueryBinOrAsciiFloatArray("FORM ASC;:CHAN1:DATA?"); // Query ascii or binary data
                Console.WriteLine($"Instrument returned {waveformAsc.Length} samples in the waveformASC array");
                // -----------------------------------------------------------
                // Fetching the trace in Binary format
                // Transfer of traces in binary format is faster.
                // The waveformBIN data and waveformASC data are however the same.
                // -----------------------------------------------------------
                instr.Binary.FloatNumbersFormat = InstrBinaryFloatNumbersFormat.Single4Bytes;
                double[] waveformBin = instr.Binary.QueryBinOrAsciiFloatArray("FORM REAL,32;:CHAN1:DATA?"); // Query ascii or binary data
                Console.WriteLine($"Instrument returned {waveformBin.Length} samples in the waveformBIN array");
                // -----------------------------------------------------------
                // Making an instrument screenshot and transferring the file to the PC
                // -----------------------------------------------------------
                instr.WriteString("HCOP:DEV:LANG PNG"); // Set the screenshot format
                instr.WriteString(@"MMEM:NAME 'c:\temp\Dev_Screenshot.png'"); // Set the screenshot path
                instr.WriteString("HCOP:IMM"); // Make the screenshot now
                instr.QueryOpc(); // Wait for the screenshot to be saved
                instr.File.FromInstrumentToPc(@"c:\temp\Dev_Screenshot.png", @"c:\Temp\PC_Screenshot.png"); // Read the response and store to the file in PC
                Console.WriteLine(@"Screenshot file saved to PC 'c:\Temp\PC_Screenshot.png'");
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