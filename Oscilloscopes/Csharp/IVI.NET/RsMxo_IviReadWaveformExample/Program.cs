using System;
using Ivi.Driver;
using Ivi.Scope;

//--------------------------------------------------------------------------
// Name:        IviReadWaveformExample
//
// Purpose:     IviScope sample program to demonstrate:
//              - Basic setting of the MXO for acquisition
//              - Performing one acquisition on Channel 1 - the timebase is set to 50us, to acquire 1kHz signal from the arb generator or the probe compensation.
//              - Fetching the waveform to the control PC
//              - Performing two measurments - Vpp and Frequency
//
//              Notice, there is no reference to the Rohde & Scharz RsMxo instrument driver.
//              The example uses only the standard IviScope and IviDriver interfaces,
//              hence, it can be used with any driver implementing IviScope.
//              Therefore, you need to tell the program to use the RsMxo. This is done via the Ivi Config Store:
//              - Open the NI MAX, select the Tree item IVI Drivers.
//              - Create a new Driver Session named "myMxoSession".
//                  - In 'Hardware tab', add a new Hardware Asset with your MXO resource name, e.g.: "TCPIP::10.205.0.159::hislip0".
//                    Name of the asset is not important, it is just for you to identify the instrument better. Make sure you check the asset's checkbox.
//                  - In 'Software Tab', select the Software Module 'RohdeSchwarz.RsMxo....Fx40'.
//                    If you do not see it in the selection, make sure you have installed the Rohde & Schwarz RsMxo IVI.NET driver.
//              - Create a new logical name "myMxo" that we will use in our program in the method IviScope.Create().
//                  For its 'Driver Session', select the newly created 'myMxoSession'.
//              - Make sure you save the that IVI Store configuration before starting this example.
//
// Prerequisites:
//
//   This sample program needs IVI Shared Components and IVI.NET Shared Components being installed.
//   To dowload them, go to http://www.ivifoundation.org/shared_components/Default.aspx
//
//   Download and install
//     - IVI Shared Components 3.0.0 or newer
//     - IVI.NET Shared Components 2.0.0 or newer
//     - Rohde & Schwarz RsMxo IVI.NET driver 1.2.0 or newer
//
//--------------------------------------------------------------------------

namespace IviReadWaveformExample
{
    static class Program
    {
        static void Main()
        {
            var scope = IviScope.Create("myMxo", false, false);
            Console.WriteLine($"Driver: {scope.Identity.Identifier}");

            var waveform = scope.Measurement.CreateWaveformDouble(50000);
            for (int i = 0; i < 1000; i++)
            {
                Console.WriteLine($"\n-------------------------------------------\n Loop count: {i+1}:\n-------------------------------------------\n");

                scope.Channels["CH1"].Enabled = true;
                scope.Trigger.Configure(Ivi.Scope.TriggerType.Edge, PrecisionTimeSpan.FromSeconds(0.001));
                scope.Acquisition.ConfigureRecord(PrecisionTimeSpan.FromSeconds(0.005), 50_000, PrecisionTimeSpan.Zero);
                scope.Trigger.Continuous = false;

                scope.Channels["CH1"].Range = 10;

                // Acquisition of the waveform
                scope.Measurement.Initiate();
                waveform = scope.Channels["CH1"].Measurement.FetchWaveform(waveform);
                Console.WriteLine($"Successfully acquired waveform with {waveform.ValidPointCount} points");

                // Waveform Measurements - no new acquisitions
                // Vpp measurement
                var res = scope.Channels["CH1"].Measurement.FetchWaveformMeasurement(MeasurementFunction.VoltagePeakToPeak);
                Console.WriteLine($"Waveform Measurement Vpp: {res} V");
                // Frequency measurement
                res = scope.Channels["CH1"].Measurement.FetchWaveformMeasurement(MeasurementFunction.Frequency);
                Console.WriteLine($"Waveform Measurement Frequency: {res} Hz");
            }
            
            scope.Close();

            Console.WriteLine("\n\nPress any key to finish ...");
            Console.ReadKey();
        }
    }
}
