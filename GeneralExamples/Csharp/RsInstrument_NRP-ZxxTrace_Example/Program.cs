// RsInstrument example for reading a trace from the legacy NRP-Zxx powersensors
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
                instr.WriteString("INIT:CONT OFF");// Switch OFF the continuous sweep
                //-----------------------------------------------------------
                // Basic Settings:
                //-----------------------------------------------------------
                instr.WriteString("*RST");
                instr.WriteString("INIT:CONT OFF");
                instr.WriteString("SENS:FUNC \"XTIM:POW\"");
                instr.WriteString("SENS:TRAC:POIN 8191");
                instr.WriteString("SENS:TRAC:TIME 20.0e-3");
                instr.WriteString("SENS:AVER:COUN:AUTO OFF");
                instr.WriteString("SENS:AVER:COUN 2");
                instr.WriteString("SENS:AVER:STAT ON");
                instr.WriteString("TRIG:SOUR IMM");
                instr.WriteString("TRIG:LEV 100e-6");
                instr.WriteString("TRIG:DEL -5.0e-6");
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
                var response = instr.QueryString("FETCH?").Split(',');
                var results = Array.ConvertAll(response.ToArray(), Convert.ToDouble);
                Console.WriteLine($"Measured samples: #{results.Length}");
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