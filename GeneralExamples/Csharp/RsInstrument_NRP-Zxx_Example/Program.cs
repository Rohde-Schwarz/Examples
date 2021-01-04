// RsInstrument example for the legacy NRP-Zxx powersensors
// - Installed Rohde & Schwarz VISA 5.12.3+ https://www.rohde-schwarz.com/appnote/1dc02
// - Installed NRP Toolkit 4.20+ https://www.rohde-schwarz.com/software/nrp-toolkit/

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using RohdeSchwarz.RsInstrument; // .NET component providing all the necessary VISA extended functionalities. Install as NuGet from www.nuget.org

namespace RsInstrument_NrpZxx_Example
{
    class Program
    {
        static void Main()
        {
            RsInstrument instr;
            RsInstrument.AssertMinVersion("1.8.0");

            try // Separate try-catch for initialization prevents accessing uninitialized object
            {
                //-----------------------------------------------------------
                // Initialization:
                //-----------------------------------------------------------

                // Adjust the VISA Resource string to fit your instrument
                // You need the R&S VISA preference in order to use the legacy NRP-Zxx sensors
                instr = new RsInstrument("USB::0x0aad::0x0095::104015::INSTR", false, false, "PreferRsVisa = True");
                instr.VisaTimeout = 3000; // Timeout for VISA Read Operations
                instr.OpcTimeout = 15000; // Timeout for opc-synchronised operations
                instr.InstrumentStatusChecking = true; // Error check after each command (default is true)
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
                instr.WriteString("*RST"); // Reset the instrument, clear the Error queue
                instr.WriteString("INIT:CONT OFF"); // Switch OFF the continuous sweep
                //-----------------------------------------------------------
                // Basic Settings:
                //-----------------------------------------------------------
                instr.WriteString("SENS:FUNC \"POW:AVG\"");
                instr.WriteString("SENS:FREQ 1e9");
                instr.WriteString("SENS:AVER:COUNT:AUTO OFF");
                instr.WriteString("SENS:AVER:COUN 16");
                instr.WriteString("SENS:AVER:STAT ON");
                instr.WriteString("SENS:AVER:TCON REP");
                instr.WriteString("SENS:POW:AVG:APER 5e-3");
                // -----------------------------------------------------------
                // SyncPoint 'SettingsApplied' - all the settings were applied
                // -----------------------------------------------------------
                instr.WriteString("INIT:IMM"); // Start the sweep

                // Wait for the measurement to finish loop
                // 200 x 20ms results in cca 4000 ms timeout
                int i;
                for (i = 0; i < 200; i++)
                {
                    int status = instr.QueryInteger("STAT:OPER:COND?");
                    if ((status & 16) == 0)
                    {
                        // Status register bit 4 signals MEASURING status
                        // Finished measuring, break
                        i = -1;
                        break;
                    }

                    Thread.Sleep(20);
                }

                if (i > 0)
                    throw new TimeoutException("Measurement timeout");

                // -----------------------------------------------------------
                // Fetching the results, format does not matter, the driver function always parses it correctly
                // -----------------------------------------------------------
                instr.WriteString("FORMAT ASCII");
                string[] results = instr.QueryString("FETCH?").Split(',').ToArray();
                // Only the first number is relevant for this measurement
                double powerWatt = double.Parse(results[0]);
                // Coerce to 1e-18 if a smaller number is returned
                powerWatt = Math.Max(powerWatt, 1e-18);
                double powerdBm = 10 * Math.Log10(powerWatt / 1e-3);
                Console.WriteLine($"Measured power: {powerWatt} Watt, {powerdBm} dBm");
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