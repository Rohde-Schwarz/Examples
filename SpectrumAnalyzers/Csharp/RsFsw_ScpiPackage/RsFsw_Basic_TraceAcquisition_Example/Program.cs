using System;
using System.ComponentModel;
using System.Reflection;
using System.Linq;
using RohdeSchwarz.RsFsw;

namespace RsFsw_Basic_TraceAcquisition_Example
{
    class Program
    {
        static void Main(string[] args)
        {
            var fsw = new RsFsw("TCPIP::localhost::HISLIP", true, true, "PreferRsVisa=True");

            // Greetings, stranger...
            Console.WriteLine($"Hello, I am: {fsw.Utilities.Identification.IdnString}");

            // Select or create the Specan Channel 
            fsw.Instrument.Select.Value = ChannelTypeEnum.SpectrumAnalyzer;

            fsw.Instrument.Select.Value = ChannelTypeEnum.K7_AnalogModulation;
            var name = fsw.K7AnalogDemod.Layout.Add.Window.Get("Janik", WindowDirectionEnum.BELow, WindowTypeK7enum.AmTimeDomain);
            //   INITiate:CONTinuous
            fsw.Initiate.Continuous.Set(false);
            Console.WriteLine($"We always work in single-sweep mode around here!");

            //   SENSe.FREQuency:STARt 100000000
            fsw.Sense.Frequency.Start = 100E6;
            
            //   SENSe.FREQuency:STOP 200000000
            fsw.Sense.Frequency.Stop = 200E6;

            //   DISPlay[:WINDow<n>]:TRACe<t>:Y[:SCALe]:RLEVel
            fsw.Display.Window.Trace.Y.Scale.RefLevel.Set(20);
            fsw.Display.Window.Subwindow.Trace.Y.Scale.Set(60);

            fsw.Display.Window.Subwindow.Trace.Mode.Set(TraceModeCenum.MAXHold, WindowRepCap.Nr1, SubWindowRepCap.Empty, TraceRepCap.Tr2);
            fsw.Display.Window.Subwindow.Trace.Mode.Set(TraceModeCenum.MINHold, WindowRepCap.Nr1, SubWindowRepCap.Empty, TraceRepCap.Tr3);

            //  INITiate:IMMediate
            fsw.Initiate.ImmediateAndWait();

            //  FORMat:DATA REAL,32
            fsw.Format.Data = DataFormatEnum.Real32;
            var dataFormat = fsw.Format.Data;

            //               TRACE:DATA? TRACe1
            var traceA = fsw.Trace.Data.Get(TraceNumberEnum.TRACe1, WindowRepCap.Nr1);
            //               TRACE:DATA? TRACe2
            var traceB = fsw.Trace.Data.Get(TraceNumberEnum.TRACe2, WindowRepCap.Empty);

            //               TRACE:DATA? TRACe3
            var traceC = fsw.Trace.Data.Get(TraceNumberEnum.TRACe3, WindowRepCap.Empty);

            fsw.Trace.RepCapWindow = WindowRepCap.Nr2;
            //               TRACE2:DATA? TRACe2
            var traceD = fsw.Trace.Data.Get(TraceNumberEnum.TRACe2);

            // Close the instrument
            fsw.Dispose();
        }
    }
}
