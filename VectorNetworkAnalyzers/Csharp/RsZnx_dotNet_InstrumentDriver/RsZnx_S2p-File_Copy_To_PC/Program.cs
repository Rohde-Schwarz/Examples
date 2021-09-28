// This program performs the calibration of the ZNx Vector Signal Generator.
// The basis for this program is a python plain SCPI script that you can find here:
// https://github.com/Rohde-Schwarz/Examples/blob/main/GeneralExamples/Python/RsInstrument/RsInstrument_ZNB_S2P-file_copy_to_PC.py
// Preconditions:
// - installed RsZnx IVI.NET instrument driver 3.30.0 or newer
// - installed R&S VISA 5.12.3+ or any other VISA

using System;
using System.IO;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using RohdeSchwarz.RsZnx;

namespace RsZnx_S2p_File_Copy_To_PC
{
    class Program
    {
        static void Main(string[] args)
        {
            var io = new RsZnx("TCPIP::10.205.0.172::INSTR", true, true, "DriverSetup=(PreferRsVisa = True)");
            // RF Setup first
            io.GeneralSettings.DisplayUpdateEnabled = DisplayUpdate.On;
            var channel1 = io.Channel.Channels["CH1"];
            channel1.Stimulus.FrequencyStart = 700E6;
            channel1.Stimulus.FrequencyStop = 1.3E9;
            channel1.Sweep.NumberOfPoints = 501;

            // Prepare S11 measurement in diagram 1
            // The very first trace do not need the AddTraceDiagramArea() to feed it into the diagram
            channel1.Meas.SParameters.SelectSParameters("Trc1", 1, 1);
            channel1.Format.TraceFormat = TraceFormat.dBMag;
            // Notice the order - first add the trace to the diagram, then configure it.
            channel1.Trace.AddTraceDiagramArea("Trc2", 1);
            channel1.Meas.SParameters.SelectSParameters("Trc2", 1, 1);
            channel1.Format.TraceFormat = TraceFormat.Phase;
            

            // Prepare S22 measurement in diagram 2 like for S11 if not separately commented
            io.Display.Diagram.AddDiagram(2);
            channel1.Trace.AddTraceDiagramArea("Trc3", 2);
            channel1.Meas.SParameters.SelectSParameters("Trc3", 2, 2);
            channel1.Format.TraceFormat = TraceFormat.dBMag;
            channel1.Trace.AddTraceDiagramArea("Trc4", 2);
            channel1.Meas.SParameters.SelectSParameters("Trc4", 2, 2);
            channel1.Format.TraceFormat = TraceFormat.Phase;

            // Prepare S21 measurement in diagram 3 like for before
            io.Display.Diagram.AddDiagram(3);
            channel1.Trace.AddTraceDiagramArea("Trc5", 3);
            channel1.Meas.SParameters.SelectSParameters("Trc5", 2, 1);
            channel1.Format.TraceFormat = TraceFormat.dBMag;
            channel1.Trace.AddTraceDiagramArea("Trc6", 3);
            channel1.Meas.SParameters.SelectSParameters("Trc6", 2, 1);
            channel1.Format.TraceFormat = TraceFormat.Phase;

            // Prepare S21 measurement in diagram 3 like for before
            io.Display.Diagram.AddDiagram(4);
            channel1.Trace.AddTraceDiagramArea("Trc7", 4);
            channel1.Meas.SParameters.SelectSParameters("Trc7", 1, 2);
            channel1.Format.TraceFormat = TraceFormat.dBMag;
            channel1.Trace.AddTraceDiagramArea("Trc8", 4);
            channel1.Meas.SParameters.SelectSParameters("Trc8", 1, 2);
            channel1.Format.TraceFormat = TraceFormat.Phase;

            // Single measurement
            channel1.Sweep.ContinuousMode = false;
            channel1.Sweep.StartSynchronized();

            // Save results to an instrument file
            var instrPath = @"C:\Users\Public\Documents\Rohde-Schwarz\Vna\Traces\s2pfile.s2p";
            channel1.Trace.TraceData.ExportDataPorts(instrPath, OutputFormat.ComplexValues, ImpedanceMode.Common, new int[] { 1, 2 });
            
            // Transfer the created file to the control PC
            var pcPath = Path.GetTempPath() + @"\pc_s2pfile.s2p";
            io.System.ReadToFileFromInstrument(instrPath, pcPath);
            io.Dispose();

            Console.WriteLine("We saved your trace file here:\n" + pcPath);

            Console.WriteLine("\nPress any key to finish");
            Console.ReadKey();
        }
    }
}
