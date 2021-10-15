// C# Example for RTB2000 / RTM2000 / RTM3000 / RTA4000 Oscilloscopes
// Preconditions:
// - Installed Rohde & Schwarz VISA 5.12.3+ https://www.rohde-schwarz.com/appnote/1dc02
// - You can also work without VISA by using LAN SocketIO - see Hello_World example

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using RohdeSchwarz.RsInstrument; // .NET component providing all the necessary VISA extended functionalities. Install as NuGet from www.nuget.org

namespace RsInstrument_RTB2000_Example
{
    class Program
    {
        static void Main()
        {
            RsInstrument instr;
            RsInstrument.AssertMinVersion("1.14.0");

            try // Separate try-catch for initialization prevents accessing uninitialized object
            {
                //-----------------------------------------------------------
                // Initialization:
                //-----------------------------------------------------------
                // Adjust the VISA Resource string to fit your instrument
                instr = new RsInstrument("TCPIP::10.112.1.140::INSTR");
                //rtb = new RsInstrument("USB0::0x0AAD::0x01D6::101457::INSTR");
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
                instr.ClearStatus(); // Clear instrument status - errors and io buffers
                Console.WriteLine($"Instrument Identification string:\n{instr.Identification.IdnString}");
                instr.WriteString("*RST"); // Reset the instrument
                instr.QueryOpc(); // Wait for the reset to finish
                //-----------------------------------------------------------
                // Basic Settings:
                //---------------------------- -------------------------------
                instr.WriteString("TIM:ACQT 0.01"); // 10ms Acquisition time
                instr.WriteString("CHAN1:RANG 5.0"); // Horizontal range 5V (0.5V/div)
                instr.WriteString("CHAN1:OFFS 0.0"); // Offset 0
                instr.WriteString("CHAN1:COUP ACL"); // Coupling AC 1MOhm
                instr.WriteString("CHAN1:STAT ON"); // Switch Channel 1 ON
                //-----------------------------------------------------------
                // Trigger Settings:
                //-----------------------------------------------------------
                instr.WriteString("TRIG:A:MODE AUTO"); // Trigger Auto mode in case of no signal is applied
                instr.WriteString("TRIG:A:TYPE EDGE;:TRIG:A:EDGE:SLOP POS"); // Trigger type Edge Positive
                instr.WriteString("TRIG:A:SOUR CH1"); // Trigger source CH1
                instr.WriteString("TRIG:A:LEV1 0.05"); // Trigger level 0.05V
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
                double[] waveformBin = instr.Binary.QueryBinOrAsciiFloatArray("FORM:BORD LSBF;:FORM REAL;:CHAN1:DATA?");
                Console.WriteLine($"Instrument returned {waveformBin.Length} samples in the waveformBIN array");

                // -----------------------------------------------------------
                // Making an instrument screenshot and transferring the file to the PC
                // -----------------------------------------------------------

                instr.WriteString("MMEM:CDIR '/INT/'"); // Change the directory

                // ignore errors generated by the MMEM:DEL command, the error is generated if the file does not exist
                instr.InstrumentStatusChecking = false;
                instr.WriteString("MMEM:DEL 'Dev_Screenshot.png'"); // Delete the file if it already exists, otherwise you get 'Execution error'
                instr.QueryOpc();
                instr.ClearStatus();
                instr.InstrumentStatusChecking = true;

                instr.WriteString("HCOP:LANG PNG;:MMEM:NAME 'Dev_Screenshot'"); // Hardcopy settings for taking a screenshot - notice no file extention here
                instr.WriteString("HCOP:IMM"); // Make the screenshot now
                instr.QueryOpc(); // Wait for the screenshot to be saved
                instr.File.FromInstrumentToPc("Dev_Screenshot.png", @"c:\Temp\PC_Screenshot.png"); // Query the instrument file
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