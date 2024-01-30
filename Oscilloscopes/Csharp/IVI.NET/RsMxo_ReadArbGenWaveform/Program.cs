using System;
using System.Diagnostics;
using System.Threading;
using Ivi.Driver;
using Ivi.Scope;

// To use the namespace RohdeSchwarz.RsMxo, add the reference to the last version of the RohdeSchwarz.RsMxo.Fx40 assembly
// with ProjectItem 'References'->RightClick->AddReference->Search 'rsmxo'
// If not found, add them from here (AnyCpu): 
// "c:\Program Files\IVI Foundation\IVI\Microsoft.NET\Framework64\v4.0.30319\RohdeSchwarz.RsMxo 1.4.0\RohdeSchwarz.RsMxo.Fx40.dll"
using RohdeSchwarz.RsMxo;
using Slope = RohdeSchwarz.RsMxo.Slope;
using TriggerSource = RohdeSchwarz.RsMxo.TriggerSource;
using TriggerType = RohdeSchwarz.RsMxo.TriggerType;
using VerticalCoupling = RohdeSchwarz.RsMxo.VerticalCoupling;

//--------------------------------------------------------------------------
// Prerequisites
//
//   This sample program needs IVI Shared Components and IVI.NET Shared Components being installed.
//   To download them, go to http://www.ivifoundation.org/shared_components/Default.aspx
//
//   Download and install
//     - IVI Shared Components 3.0.0 or newer
//     - IVI.NET Shared Components 2.0.0 or newer
//     - Rohde & Schwarz RsMxo IVI.NET driver 1.2.0 or newer
//
//--------------------------------------------------------------------------

namespace ReadArbGenWaveform
{
    internal class Program
    {
        static void Main()
        {
            bool reset = true;
            var mxo = new RsMxo("TCPIP::10.112.0.37::hislip0", false, reset);

            // General settings
            mxo.Settings.System.Remote.DisplayUpdateEnabled = true;
            mxo.Settings.System.Remote.DisplayUpdateEnabled = true;

            // Channel 1 settings
            var mxoCh1Ver = mxo.Vertical[RepCapChannel.CH1];
            mxoCh1Ver.ShowChannel = true;
            mxoCh1Ver.Scale = 0.5; // 0.5 Volts/div
            mxoCh1Ver.Offset = 0;
            mxoCh1Ver.Coupling = VerticalCoupling.DCLimit;
            mxo.Horizontal.TimeScale = 0.01;
            mxo.Acquisition.RecordLengthMode = AcquisitionRecordLengthMode.Auto;
            mxo.Acquisition.RecordLengthLimit = 100E3;
            
            // Trigger settings
            var mxoTrig = mxo.Trigger.Event[RepCapTriggerEvent.TrigA];
            mxo.Trigger.Mode = TriggerMode.Normal;
            mxoTrig.Source = TriggerSource.Channel1;
            mxoTrig.Type = TriggerType.Edge;
            mxoTrig.Edge.Slope = Slope.Negative;
            mxoTrig.Channel[RepCapChannel.CH1].Level = 0.4;

            // MXO Arbitrary Generator settings
            var mxoGen = mxo.Generator[RepCapGenerator.Gen1];
            mxoGen.State = false;
            mxoGen.FunctionType = GeneratorFunctionType.Pulse;
            mxoGen.Frequency = 0.1;
            mxoGen.Amplitude = 1.0;
            mxoGen.PulseWidth = 1.0;
            mxoGen.State = true;

            // Acquisition
            mxo.Acquisition.RunSingleNoWait();

            var watch = new Stopwatch();
            watch.Start();
            while (true)
            {
                var armed = (mxo.UtilityFunctions.QueryInt32("STAT:OPER:COND?") & 0x30) == 0x30;
                if (armed)
                    break;

                Thread.Sleep(5);
            }
            watch.Stop();
            Console.WriteLine($"Waiting for ARMED: {watch.ElapsedMilliseconds} ms");

            // Waiting for measurement complete
            watch.Reset();
            watch.Start();
            while (true)
            {
                var measComplete = (mxo.UtilityFunctions.QueryInt32("STAT:OPER:COND?") & 0x10) == 0;
                if (measComplete)
                    break;

                Thread.Sleep(5);
            }
            watch.Stop();
            Console.WriteLine($"Waiting for MEAS_COMPLETE: {watch.ElapsedMilliseconds} ms");

            var waveform = mxo.WaveformAcquisition.Channel[RepCapChannel.CH1].FetchChannelWaveform();
            Console.WriteLine($"Waveform start {waveform.StartTime}, duration {waveform.TotalTime}, record length {waveform.ValidPointCount}");
            Console.WriteLine("Press any key to exit");
            Console.ReadKey();
        }
    }
}
