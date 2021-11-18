// This program performs segmented sweep for 2 Channels on a ZNx Vector Signal Generator.
// The basis for this program is a python plain SCPI script that you can find here:
// https://github.com/Rohde-Schwarz/Examples/blob/main/VectorNetworkAnalyzers/Python/RsInstrument/RsInstrument_ZNB_Segmented_Sweep_2channels.py
// Preconditions:
// - installed RsZnx IVI.NET instrument driver 3.35.0 or newer
// - installed R&S VISA 5.12.3+ or any other VISA


using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using RohdeSchwarz.RsZnx;

namespace RsZnx_Segmented_Sweep_2Channels
{
    class Program
    {
        static void Main(string[] args)
        {
            var io = new RsZnx("TCPIP::10.205.0.51::INSTR", true, true);

            // Be sure to have the display updated whilst remote control
            io.GeneralSettings.DisplayUpdateEnabled = DisplayUpdate.On;

            // -------------------------- Channel 1 ----------------------------------

            // First, we are addressing the Channel 1
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
            var sgm1 = ch1.Sweep.Segment["Seg1"];
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


            // -------------------------- Channel 2 ----------------------------------

            // Adding Diagram 2, Channel 2, and Trace 2 (Name 'Ch2Tr2')
            io.Display.Diagram.AddDiagram(2);
            io.Channel.AddChannel(2, "CH2");
            var ch2 = io.Channel.Channels[RepCapChannel.CH2];
            ch2.Trace.AddTrace("Ch2Tr2", "'S22'");
            ch2.Trace.AssignTraceDiagramArea("Ch2Tr2", 2);



            //# Using the complete command including "SENSe" will define the channel the changes will be associated to
            //            Instrument.write_str_with_opc("CALCULATE2:PARAMETER:SDEFINE 'Trc2', 'S21'")
            //    Instrument.write_str_with_opc("CALCULATE2:PARAMETER:SELECT 'Trc2'")
            //    Instrument.write_str_with_opc("DISPLAY:WINDOW2:STATE ON")
            //    Instrument.write_str_with_opc("DISPLAY:WINDOW2:TRACE1:FEED 'Trc2'")
            //
            //   Instrument.write_str_with_opc("SENSe2:SEGment:CLEar")                                                   # Deletes all sweep segments in CH2

            // First, we are addressing the Channel 1
            // Set single sweep mode
            ch2.Sweep.ContinuousMode = false;

            // Auto Sweep time
            ch2.Sweep.TimeAuto = true;

            // Trigger immediate (Auto)
            ch2.Trigger.Source = TriggerSource.FreeRun;

            // Averaging disabled
            ch2.Average.State = false;

            // Deletes all sweep segments in the channel
            ch2.Sweep.SegmentDeleteAll();

            // Define Segment 1
            ch2.Sweep.AddSegment(1);
            sgm1 = ch2.Sweep.Segment[RepCapSegment.Seg1];
            sgm1.FrequencyStart = 100E6;
            sgm1.FrequencyStop = 500E6;
            sgm1.Points = 401;
            sgm1.Power = 10;
            sgm1.Bandwidth = 500;

            // Define Segment 2
            ch2.Sweep.AddSegment(2);
            sgm2 = ch2.Sweep.Segment[RepCapSegment.Seg2];
            sgm2.FrequencyStart = 2000E6;
            sgm2.FrequencyStop = 2100E6;
            sgm2.Points = 101;
            sgm2.Power = 0;
            sgm2.Bandwidth = 1000;

            // Change mode to frequency segmented operations
            ch2.Sweep.Type = SweepType.Segmented;


            // Start the sweep on all channels, wait for them to finish
            // The channel you use is irrelevant
            // If you do not want to wait for the sweep to finish, use the ch1.Sweep.StartAll()
            ch1.Sweep.StartAllSynchronized();

            // To Start a sweep channel-wise:
            // ch1.Sweep.StartSynchronized() or ch1.Sweep.Start()

            // ---------------------------- Read the results of Channel 1 ------------------
            
            // Trace Data
            var data1 = ch1.Trace.TraceData.ResponseData(DataFormat.Unformatted);
            Console.WriteLine($"Channel 1 trace data size: {data1.Length}");

            // Marker Max
            ch1.Marker[RepCapMarker.Mk1].Enabled = true;
            ch1.Marker[RepCapMarker.Mk1].Search.MarkerSearch(MarkerSearch.Maximum);
            var result1MkMax = ch1.Marker[RepCapMarker.Mk1].Search.Result();
            Console.WriteLine($"Channel 1 Marker 1 Max: {result1MkMax.stimulus:F3} Hz, {result1MkMax.response[0]:F3} dB");

            // Marker Min
            ch1.Marker[RepCapMarker.Mk2].Enabled = true;
            ch1.Marker[RepCapMarker.Mk2].Search.MarkerSearch(MarkerSearch.Minimum);
            var result1MkMin = ch1.Marker[RepCapMarker.Mk2].Search.Result();
            Console.WriteLine($"Channel 1 Marker 2 Min: {result1MkMin.stimulus:F3} Hz, {result1MkMin.response[0]:F3} dB");

            // Marker concrete frequency
            ch1.Marker[RepCapMarker.Mk3].Enabled = true;
            ch1.Marker[RepCapMarker.Mk3].Stimulus = 2E9;
            var result1MkDed = ch1.Marker[RepCapMarker.Mk3].Response;
            Console.WriteLine($"Channel 1 Marker 3 concrete: 2 GHz, {result1MkDed:F3} dB");

            // ---------------------------- Read the results of Channel 1 ------------------

            // Trace Data
            var data2 = ch2.Trace.TraceData.ResponseData(DataFormat.Unformatted);
            Console.WriteLine($"Channel 2 trace data size: {data2.Length}");

            // Marker Max
            ch2.Marker[RepCapMarker.Mk1].Enabled = true;
            ch2.Marker[RepCapMarker.Mk1].Search.MarkerSearch(MarkerSearch.Maximum);
            var result2MkMax = ch2.Marker[RepCapMarker.Mk1].Search.Result();
            Console.WriteLine($"Channel 2 Marker 1 Max: {result2MkMax.stimulus:F3} Hz, {result2MkMax.response[0]:F3} dB");

            // Marker Min
            ch2.Marker[RepCapMarker.Mk2].Enabled = true;
            ch2.Marker[RepCapMarker.Mk2].Search.MarkerSearch(MarkerSearch.Minimum);
            var result2MkMin = ch2.Marker[RepCapMarker.Mk2].Search.Result();
            Console.WriteLine($"Channel 2 Marker 2 Min: {result2MkMin.stimulus:F3} Hz, {result2MkMin.response[0]:F3} dB");

            // Marker concrete frequency
            ch2.Marker[RepCapMarker.Mk3].Enabled = true;
            ch2.Marker[RepCapMarker.Mk3].Stimulus = 300E6;
            var result2MkDed = ch2.Marker[RepCapMarker.Mk3].Response;
            Console.WriteLine($"Channel 2 Marker 3 concrete: 300 MHz, {result2MkDed:F3} dB");

            Console.WriteLine("\nPress any key to finish");
            Console.ReadKey();
        }
    }
}
