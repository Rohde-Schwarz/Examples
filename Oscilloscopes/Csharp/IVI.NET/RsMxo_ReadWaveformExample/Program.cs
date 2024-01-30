using System;
using Ivi.Driver;
using Ivi.Scope;

// To use the namespace RohdeSchwarz.RsMxo, add the reference to the last version of the RohdeSchwarz.RsMxo.Fx40 assembly
// with ProjectItem 'References'->RightClick->AddReference->Search 'rsmxo'
// If not found, add them from here (AnyCpu): 
// "c:\Program Files\IVI Foundation\IVI\Microsoft.NET\Framework64\v4.0.30319\RohdeSchwarz.RsMxo 1.2.0\RohdeSchwarz.RsMxo.Fx40.dll"
using RohdeSchwarz.RsMxo;

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

namespace ReadWaveformExample
{
    static class Program
    {
        [STAThread]
        static void Main()
        {
            bool reset = true;
            var mxo = new RsMxo("TCPIP::10.205.0.159::hislip0", false, reset);
            const double freq = 1e3;
            const double amp = 2;
            
            // Setting up the MXO Generator
            mxo.Generator[RepCapGenerator.Gen1].FunctionType = GeneratorFunctionType.Sinusoid;
            mxo.Generator[RepCapGenerator.Gen1].Frequency = freq;
            mxo.Generator[RepCapGenerator.Gen1].Amplitude = amp;
            mxo.Generator[RepCapGenerator.Gen1].State = true;

            mxo.Vertical["CH1"].ShowChannel = true;
            mxo.Vertical["CH1"].Scale = 1.0; // 1.0 Volts/div
            mxo.Trigger.Event["TrigA"].Type = RohdeSchwarz.RsMxo.TriggerType.Edge;
            mxo.Trigger.Holdoff.Mode = TriggerHoldoffMode.Time;
            mxo.Trigger.Holdoff.Time = 0.001;

            // Timebase is set to 50us, to acquire 1kHz signal from the arb generator or the probe compensation output
            mxo.Acquisition.SampleRateMode = AcquisitionSampleRateMode.Auto;
            mxo.Horizontal.Position = 0;
            mxo.Horizontal.TimeScale = 500e-6; // 500us/div

            // Measurements configuration: Vpp and Frequency
            var meas1 = mxo.Meas[RepCapMeasurement.Measurement1];
            meas1.MeasurementSource(MeasurementSource.Channel1, MeasurementSource.None);
            meas1.MeasurementType = MeasurementType.PeakDelta;
            meas1.Enabled = true;

            var meas2 = mxo.Meas[RepCapMeasurement.Measurement2];
            meas2.MeasurementSource(MeasurementSource.Channel1, MeasurementSource.None);
            meas2.MeasurementType = MeasurementType.Frequency;
            meas2.Enabled = true;

            // Starting one acquisition and waiting for it to finish. Use OPC timeout.
            mxo.Acquisition.RunSingle();

            // Fetch the waveform
            var waveform = mxo.WaveformAcquisition.FetchWaveformDouble(Source.Channel1);
            Console.WriteLine($"Successfully acquired waveform with {waveform.ValidPointCount} points");
            
            // Measurements queries
            double res1 = meas1.Results.Statistics.Current;
            Console.WriteLine($"Waveform Measurement Vpp: {res1} V");
            double res2 = meas2.Results.Statistics.Current;
            Console.WriteLine($"Waveform Measurement Frequency: {res2} Hz");
            mxo.Close();

            Console.WriteLine("\n\nPress any key to finish ...");
            Console.ReadKey();
        }
    }
}
