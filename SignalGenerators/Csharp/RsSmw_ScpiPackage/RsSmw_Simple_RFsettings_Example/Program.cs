// Basic example on how to work with R&S RsSmw driver package
// The example does the following:
// - Initializes the session - see the commented lines on how to initialize the session with the specified VISA or no VISA at all
// - Reads the standard information of the instrument
// - Shows the cloning and using the RepCapHwInstance for having two objects one for Output A and one for Output B
// - Does couple of standard RF settings on both channels
// - Shows the standard SCPI write / query communication
// Make sure you:
// - Install the RsSmw driver package over Packet Manager from Nuget.org
// - Adjust the IP address the match your instrument

using System;
using RohdeSchwarz.RsSmw;

namespace RsSmw_Example
{
    class Program
    {
        static void Main()
        {
            var smw = new RsSmw("TCPIP::10.112.1.67::INSTR", true, true);
            //var smw = new RsSmw("TCPIP::10.112.1.179::INSTR", true, true, "SelectVisa=RsVisa"); // Forcing R&S VISA
            //var smw = new RsSmw("TCPIP::10.112.1.179::5025::SOCKET", true, true, "SelectVisa=SocketIo"); // No VISA needed
            Console.WriteLine("Driver Info: " + smw.Utilities.Identification.DriverVersion);
            Console.WriteLine($"Selected Visa: {smw.Utilities.Identification.VisaManufacturer}, DLL: {smw.Utilities.Identification.VisaDllName}");
            Console.WriteLine("Instrument: " + smw.Utilities.Identification.IdnString);
            Console.WriteLine("Instrument options: " + string.Join(",", smw.Utilities.Identification.InstrumentOptions));

            // Driver's instrument status checking ( SYST:ERR? ) after each command (default value is true):
            smw.Utilities.InstrumentStatusChecking = true;

            // The driver object uses the global HW instance one - RF out A
            smw.RepCapHwInstance = HwInstanceRepCap.InstA;
            
            // Clone the driver object to the driverHw2 and select the RF out B
            var smwB = smw.Clone();
            smwB.RepCapHwInstance = HwInstanceRepCap.InstB;

            // Now we have two independent objects for two RF Outputs - smw and smwB
            // They share some common features of the instrument, like for example resetting
            smw.Utilities.Reset();

            // Set the Output A to CW -20 dBm, 223 MHz
            smw.Output.State.Value = true;
            smw.Source.Frequency.Mode = FreqModeEnum.CW;
            smw.Source.Power.Level.Immediate.Amplitude = -20;
            smw.Source.Frequency.Fixed.Value = 223E6;
            Console.WriteLine($"Channel 1 PEP level: {smw.Source.Power.Pep:F2} dBm");

            // Set the Output B to frequency sweep
            smwB.Output.State.Value = false;
            smwB.Source.Frequency.Mode = FreqModeEnum.SWEep;
            smwB.Source.Power.Level.Immediate.Amplitude = -35;
            smwB.Source.Frequency.Start = 800E6;
            smwB.Source.Frequency.Stop = 900E6;
            smwB.Source.Frequency.Step.Mode = FreqStepModeEnum.DECimal;
            smwB.Source.Frequency.Step.Increment = 10E6;
            Console.WriteLine($"Channel 2 PEP level: {smwB.Source.Power.Pep:F2} dBm");

            // Direct SCPI interface is in smw.Utilities:
            var response = smw.Utilities.QueryString("*IDN?");
            Console.WriteLine($"Direct SCPI response on *IDN?: {response}");

            // Closing the session
            smw.Dispose();

            Console.Write("\n\nPress any key...");
            Console.ReadKey();
        }
    }
}
