// This program performs segmented sweep on a ZNx Vector Signal Generator.
// The basis for this program is a python plain SCPI script that you can find here:
// https://github.com/Rohde-Schwarz/Examples/blob/main/GeneralExamples/Python/RsInstrument/RsInstrument_ZNB_CAL_P1.py
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
            
            // Be sure to have the display updated whilst remote control
            io.GeneralSettings.DisplayUpdateEnabled = DisplayUpdate.On;

            // We will be addressing the Channel 1
            var ch1 = io.Channel.Channels[RepCapChannel.CH1];
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

            // Measurement

            // Change mode to frequency segmented operations
            ch1.Sweep.Type = SweepType.Segmented;
            ch1.Sweep.StartSynchronized();
            var data = ch1.Trace.TraceData.ResponseData(DataFormat.Unformatted);
            Console.WriteLine(string.Join(", ", data.Select(x => x.ToString("F3"))));

            Console.WriteLine("\nPress any key to finish");
            Console.ReadKey();
        }
    }
}
