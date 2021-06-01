// Basic example on how to work with R&S RsNgx driver package
// The example does the following:
// - Initializes the session - see the commented lines on how to initialize the session with the specified VISA or no VISA at all
// - Reads the standard information of the instrument
// - Does couple of standard Voltage and Current limit settings, and Output state
// - Switches the outputs ON
// - Measures the output Voltage and Current
// In comments above the calls, you see the SCPI commands sent. Notice, that the SCPI commands
// track the python interfaces.
// Make sure you:
// - Install the RsNgx driver package over Packet Manager from NuGet.org
// - Adjust the IP address the match your instrument

using System;
using RohdeSchwarz.RsNgx;

namespace RsNgx_Example
{
    class Program
    {
        static void Main()
        {
            var ngx = new RsNgx("TCPIP::10.102.52.45::INSTR", true, true);
            //var ngx = new RsNgx("TCPIP::10.102.52.45::INSTR", true, true, "SelectVisa=RsVisa"); // Forcing R&S VISA
            //var ngx = new RsNgx("TCPIP::10.102.52.45::5025::SOCKET", true, true, "SelectVisa=SocketIo"); // No VISA needed
            Console.WriteLine("Driver Info: " + ngx.Utilities.Identification.DriverVersion);
            Console.WriteLine("Instrument: " + ngx.Utilities.Identification.IdnString);
            Console.WriteLine("Instrument options: " + string.Join(",", ngx.Utilities.Identification.InstrumentOptions));

            // Driver's instrument status checking ( SYST:ERR? ) after each command (default value is true):
            ngx.Utilities.InstrumentStatusChecking = true;
            ngx.Utilities.Reset();

            // Master switch for all the outputs - switch OFF
            //  OUTPut:GENeral:STATe OFF
            ngx.Output.General.State = false;

            // Select and set Output 1
            //  INSTrument:SELect 1
            ngx.Instrument.Select.Set(1);
            //  SOURce:VOLTage:LEVel:IMMediate:AMPlitude 3.3
            ngx.Source.Voltage.Level.Immediate.Amplitude = 3.3;
            //  SOURce:CURRent:LEVel:IMMediate:AMPlitude 0.1
            ngx.Source.Current.Level.Immediate.Amplitude = 0.1;
            // Prepare for setting the output to ON with the master switch
            //  OUTPut:SELect ON
            ngx.Output.Select = true;

            // Select and set Output 2
            //  INSTrument:SELect 2
            ngx.Instrument.Select.Set(2);
            //  SOURce:VOLTage:LEVel:IMMediate:AMPlitude 5.1
            ngx.Source.Voltage.Level.Immediate.Amplitude = 5.1;
            //  SOURce:CURRent:LEVel:IMMediate:AMPlitude 0.05
            ngx.Source.Current.Level.Immediate.Amplitude = 0.05;
            // Prepare for setting the output to ON with the master switch
            //  OUTPut:SELect ON
            ngx.Output.Select = true;

            // The outputs are still OFF, they wait for this master switch:
            //  OUTPut:GENeral:STATe ON
            ngx.Output.General.State = true;
            // Insert a small pause to allow the instrument to settle the output
            System.Threading.Thread.Sleep(500);

            //  INSTrument:SELect 1
            ngx.Instrument.Select.Set(1);
            //                    READ?
            var measurement = ngx.Read();
            Console.WriteLine($"Measured values Output 1: {measurement.Voltage} V, {measurement.Current} A");

            //  INSTrument:SELect 2
            ngx.Instrument.Select.Set(2);
            //                READ?
            measurement = ngx.Read();
            Console.WriteLine($"Measured values Output 2: {measurement.Voltage} V, {measurement.Current} A");

            // Closing the session
            ngx.Dispose();

            Console.Write("\n\nPress any key...");
            Console.ReadKey();
        }
    }
}
