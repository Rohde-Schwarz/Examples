// This program performs segmented sweep for 1 Channel on a ZNx Vector Signal Generator.
// The basis for this program is a python plain SCPI script that you can find here:
// https://github.com/Rohde-Schwarz/Examples/blob/main/VectorNetworkAnalyzers/Python/RsInstrument/RsInstrument_ZNB_Segmented_Sweep.py
// Preconditions:
// - installed RsZnx IVI.NET instrument driver 3.35.0 or newer
// - installed R&S VISA 5.12.3+ or any other VISA


using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using RohdeSchwarz.RsZnx;

namespace RsZnx_Segmented_Sweep
{
    class Program
    {
        static void Main(string[] args)
        {
            var io = new RsZnx("TCPIP::10.205.0.51::INSTR", true, true);
            Console.WriteLine($"Hello, I am {io.System.IDQueryResponse}");

            // Be sure to have the display updated whilst remote control
            io.GeneralSettings.DisplayUpdateEnabled = DisplayUpdate.On;

            // We are addressing the Channel 1
            var ch1 = io.Channel.Channels[RepCapChannel.CH1];

            // Channel 1, Diagram 1 and Trace 1 (Name 'Trc1') exist already by default
            // Change the Trc1 Type to S11
            ch1.Trace.AddTrace("Trc1", "'S11'");
            ch1.Trace.AssignTraceDiagramArea("Trc1", 1);

            // Set single sweep mode
            ch1.Sweep.ContinuousMode = false;

            // Auto Sweep time
            ch1.Sweep.TimeAuto = true;

            // Trigger immediate (Auto)
            ch1.Trigger.Source = TriggerSource.FreeRun;

            // Averaging disabled
            ch1.Average.State = false;

            // Deletes all sweep segments in the channel
            ch1.Sweep.SegmentDeleteAll();

            // Define Segment 1
            ch1.Sweep.AddSegment(1);
            var sgm1 = ch1.Sweep.Segment[RepCapSegment.Seg1];
            sgm1.FrequencyStart = 500E6;
            sgm1.FrequencyStop = 900E6;
            sgm1.Points = 401;
            sgm1.Power = 10;
            sgm1.Bandwidth = 500;

            // Define Segment 2
            ch1.Sweep.AddSegment(2);
            var sgm2 = ch1.Sweep.Segment[RepCapSegment.Seg2];
            sgm2.FrequencyStart = 1200E6;
            sgm2.FrequencyStop = 2400E6;
            sgm2.Points = 501;
            sgm2.Power = 0;
            sgm2.Bandwidth = 1000;

            // Change mode to frequency segmented operations
            ch1.Sweep.Type = SweepType.Segmented;
            
            // Start the sweep
            ch1.Sweep.StartSynchronized();

            // Read the results - trace
            var data = ch1.Trace.TraceData.ResponseData(DataFormat.Unformatted);
            Console.WriteLine(string.Join(", ", data.Select(x => x.ToString("F3"))));

            // Marker Max
            ch1.Marker[RepCapMarker.Mk1].Enabled = true;
            ch1.Marker[RepCapMarker.Mk1].Search.MarkerSearch(MarkerSearch.Maximum);
            var resultMkMax = ch1.Marker[RepCapMarker.Mk1].Search.Result();
            Console.WriteLine($"Marker 1 Max: {resultMkMax.stimulus:F3} Hz, {resultMkMax.response[0]:F3} dB");

            // Marker Min
            ch1.Marker[RepCapMarker.Mk2].Enabled = true;
            ch1.Marker[RepCapMarker.Mk2].Search.MarkerSearch(MarkerSearch.Minimum);
            var resultMkMin = ch1.Marker[RepCapMarker.Mk2].Search.Result();
            Console.WriteLine($"Marker 2 Min: {resultMkMin.stimulus:F3} Hz, {resultMkMin.response[0]:F3} dB");

            // Marker concrete frequency
            ch1.Marker[RepCapMarker.Mk3].Enabled = true;
            ch1.Marker[RepCapMarker.Mk3].Stimulus = 2E9;
            var resultMkDed = ch1.Marker[RepCapMarker.Mk3].Response;
            Console.WriteLine($"Marker 3 concrete: 2 GHz, {resultMkDed:F3} dB");

            Console.WriteLine("\nPress any key to finish");
            Console.ReadKey();
        }
    }
}
