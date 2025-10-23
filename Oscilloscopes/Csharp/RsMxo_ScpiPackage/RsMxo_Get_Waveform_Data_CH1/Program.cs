// Basic example on how to work with R&S RsMxo driver package
// This example performs the following actions on an MXO Oscilloscope:
// - Basic configuration
// - Triggers an acquisition and waits for it to finish.
// - Fetches the waveform for Channel 1.

// Make sure you:
// - Install the RsMxo driver package over Packet Manager from Nuget.org
// - Adjust the IP address the match your instrument

using System;
using RohdeSchwarz.RsMxo; // Install with Nuget Packet Manager from Nuget.org

namespace RsMxo_Example
{
    class Program
    {
        static void Main()
        {
            var mxo = new RsMxo("TCPIP::10.103.34.37::hislip0", true, false);
            //var smab = new RsMxo("TCPIP::10.112.1.73::hislip0", true, true, "SelectVisa=RsVisa"); // Forcing R&S VISA
            //var smab = new RsMxo("TCPIP::10.112.1.73::5025::SOCKET", true, true, "SelectVisa=SocketIo"); // No VISA needed
            Console.WriteLine("Driver Info: " + mxo.Utilities.Identification.DriverVersion);
            Console.WriteLine($"Selected Visa: {mxo.Utilities.Identification.VisaManufacturer}, DLL: {mxo.Utilities.Identification.VisaDllName}");
            Console.WriteLine("Instrument: " + mxo.Utilities.Identification.IdnString);
            Console.WriteLine("Instrument options: " + string.Join(",", mxo.Utilities.Identification.InstrumentOptions));

            // Driver's instrument status checking ( SYST:ERR? ) after each command (default value is true):
            mxo.Utilities.InstrumentStatusChecking = true;
            mxo.Utilities.Reset();

            //  SYSTem:DISPlay:UPDate ON
            mxo.System.Display.Update = true;

            //  TRIGger:MODE AUTO
            mxo.Trigger.Mode = TriggerModeEnum.AUTO;
            mxo.Trigger.Event.Source.Set(TriggerSourceEnum.C1);

            //  ACQuire:SRATe:MODE AUTO
            mxo.Acquire.SymbolRate.Mode = AutoManualModeEnum.AUTO;

            // Create 'Channel' object 'ch1', that always addresses the Analog Channel 1
            var ch1 = mxo.Channel.Clone();
            ch1.RepCapChannel = ChannelRepCap.Ch1;

            // CHANnel1:STATe ON
            ch1.State.Set(true);

            // Perform the acquisition, wait for it to finish.
            //  RUNSingle;*OPC
            mxo.Run.SingleAndWait(5000);

            // CHANnel1:DATA:HEADer?
            var dataHdrCh1 = ch1.Data.Header.Get();
            Console.WriteLine($"\nChannel 1 data: header:");
            Console.WriteLine($"Time Start: {dataHdrCh1.Xstart}");
            Console.WriteLine($"Time Stop: {dataHdrCh1.Xstop}");
            Console.WriteLine($"Record Length: {dataHdrCh1.RecordLength}");
            Console.WriteLine($"Values per Sample: {dataHdrCh1.ValsPerSmp}");


            // CHANnel1:DATA:VALues?
            var wform1 = ch1.Data.Values.Get();
            Console.WriteLine($"Channel 1 data retrieved {wform1.Count} values");

            // Closing the session
            mxo.Dispose();

            Console.Write("\n\nPress any key...");
            Console.ReadKey();
        }
    }
}
