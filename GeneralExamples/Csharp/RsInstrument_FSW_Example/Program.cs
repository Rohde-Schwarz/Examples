// RsInstrument Specan Example for FSW / FSV / FPS / FSWP / FSQ Spectrum Analyzers

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using RohdeSchwarz.RsInstrument; // .NET component providing all the necessary VISA extended functionalities. Install as NuGet from www.nuget.org

namespace RsInstrument_FSW_Example
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

            try // try block to catch any RsInstrumentException()
            {
                Console.WriteLine($"RsInstrument Driver Version: {instr.Identification.DriverVersion}, Core Version: {instr.Identification.CoreVersion}");
                instr.ClearStatus(); // Clear instrument io buffers
                Console.WriteLine($"Instrument Identification string:\n{instr.Identification.IdnString}");
                instr.WriteString("*RST;*CLS"); // Reset the instrument, clear the Error queue
                instr.WriteString("INIT:CONT OFF"); // Switch OFF the continuous sweep
                instr.WriteString("SYST:DISP:UPD ON"); // Display update ON - switch OFF after debugging
                //-----------------------------------------------------------
                // Basic Settings:
                //-----------------------------------------------------------
                instr.WriteString("DISP:WIND:TRAC:Y:RLEV 10.0"); // Setting the Reference Level
                instr.WriteString("FREQ:CENT 3.0 GHz"); // Setting the center frequency
                instr.WriteString("FREQ:SPAN 200 MHz"); // Setting the span
                instr.WriteString("BAND 100 kHz"); // Setting the RBW
                instr.WriteString("BAND:VID 300kHz"); // Setting the VBW
                instr.WriteString("SWE:POIN 10001"); // Setting the sweep points
                instr.QueryOpc(); // Using *OPC? query waits until all the instrument settings are finished
                // -----------------------------------------------------------
                // SyncPoint 'SettingsApplied' - all the settings were applied
                // -----------------------------------------------------------
                instr.VisaTimeout = 2000; // Sweep timeout - set it higher than the instrument acquisition time
                instr.WriteString("INIT"); // Start the sweep
                instr.QueryOpc(); // Using *OPC? query waits until the instrument finished the acquisition
                // -----------------------------------------------------------
                // SyncPoint 'AcquisitionFinished' - the results are ready
                // -----------------------------------------------------------
                // Fetching the trace in ASCII format
                // -----------------------------------------------------------
                double[] traceAsc = instr.Binary.QueryBinOrAsciiFloatArray("FORM ASC;:TRAC? TRACE1"); // Query ascii or binary data
                Console.WriteLine($"Instrument returned {traceAsc.Length} samples in the traceAsc array");
                // -----------------------------------------------------------
                // Fetching the trace in Binary format
                // The transfer time of traces in binary format is shorter.
                // The traceBIN data and traceASC data are however the same.
                // -----------------------------------------------------------
                instr.Binary.FloatNumbersFormat = InstrBinaryFloatNumbersFormat.Single4Bytes;
                double[] traceBin = instr.Binary.QueryBinOrAsciiFloatArray("FORM REAL,32;:TRAC? TRACE1"); // Query ascii or binary data
                Console.WriteLine($"Instrument returned {traceAsc.Length} samples in the traceBin array");
                // -----------------------------------------------------------
                // Setting the marker to max and querying the X and Y
                // -----------------------------------------------------------
                instr.WriteString("CALC1:MARK1:MAX"); // Set the marker to the maximum point of the entire trace
                instr.QueryOpc(); // Using *OPC? query waits until the marker is set
                var markerX = instr.QueryDouble("CALC1:MARK1:X?");
                var markerY = instr.QueryDouble("CALC1:MARK1:Y?");
                Console.WriteLine($"Marker Frequency {markerX:F3} Hz, Level {markerY:F2} dBm");
                // -----------------------------------------------------------
                // Making an instrument screenshot and transferring the file to the PC
                // -----------------------------------------------------------
                instr.WriteString("HCOP:DEV:LANG PNG");
                instr.WriteString(@"MMEM:NAME 'c:\temp\Dev_Screenshot.png'");
                instr.WriteString("HCOP:IMM"); // Make the screenshot now
                instr.QueryOpc(); // Wait for the screenshot to be saved
                instr.File.FromInstrumentToPc(@"c:\temp\Dev_Screenshot.png", @"c:\Temp\PC_Screenshot.png"); // Query the instrument file
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