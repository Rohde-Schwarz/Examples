// This program performs the calibration of the ZNx Vector Signal Generator.
// The basis for this program is a python plain SCPI script that you can find here:
// https://github.com/Rohde-Schwarz/Examples/blob/main/GeneralExamples/Python/RsInstrument/RsInstrument_ZNB_CAL_P1.py
// Preconditions:
// - installed RsZnx IVI.NET instrument driver
// - installed RsVisa 5.12+ or any other Visa

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using RohdeSchwarz.RsZnx;

namespace RsZnx_calibration_p1
{
    class Program
    {
        static void Main(string[] args)
        {
            var io = new RsZnx("TCPIP::192.168.1.101::INSTR", true, true);
            // RF Setup first
            io.GeneralSettings.DisplayUpdateEnabled = true;
            var channel1 = io.Channel.Channels["CH1"];
            channel1.Stimulus.FrequencyStart = 1E9;
            channel1.Stimulus.FrequencyStop = 2E9;
            channel1.Sweep.NumberOfPoints = 501;
            channel1.Meas.SParameters.SelectSParameters("Trc1", 1, 1);

            // Calibration preparation setup follows
            var calibCh1 = channel1.Calibration;
            calibCh1.SelectCalibrationKit(ConnectorKit.PC292, "ZN-Z229");
            calibCh1.SelectCalibrationType("NewCal", CalibrationType.ReflOSM, new int[] { 1 }, "");
            io.System.WriteCommandWithOPCSync("SENSe:CORRection:COLLect:ACQuire:RSAVe:DEFault OFF");

            Console.WriteLine("Connect OPEN to port 1 and press any key to start the calibration ...");
            channel1.Calibration.StartCalibration(CalibrationStandard.Open, new int[] { 1 }, true, false, 0, new Ivi.Driver.PrecisionTimeSpan(20));

            Console.WriteLine("Connect SHORT to port 1 and press any key to start the calibration ...");
            calibCh1.StartCalibration(CalibrationStandard.Short, new int[] { 1 }, true, false, 0, new Ivi.Driver.PrecisionTimeSpan(20));

            Console.WriteLine("Connect MATCH to port 1 and press any key to start the calibration ...");
            calibCh1.StartCalibration(CalibrationStandard.Match, new int[] { 1 }, true, false, 0, new Ivi.Driver.PrecisionTimeSpan(20));

            calibCh1.SaveCalibrationData();
            calibCh1.CalibrationManager(CalManagerOperation.Copy, "NEWCAL.cal", null);
            calibCh1.CalibrationManager(CalManagerOperation.Apply, "NEWCAL.cal", null);

            io.Dispose();
        }
    }
}
