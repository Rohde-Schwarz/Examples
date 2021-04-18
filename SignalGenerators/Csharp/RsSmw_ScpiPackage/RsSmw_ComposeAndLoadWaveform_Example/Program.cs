// Example of creating Rohde Schwarz Waveform files, sending them to the instrument and activating them
// The example does the following:
// - Generates I/Q vectors iSamples and qSamples
// - Creates 2 waveform files out of them: pcWvFileA and pcWvFileB
// - Sends them to the instrument to BB channels A and B
// - Activates the Arbitrary generators A and B
// - Sets the RF Outputs A and B

// Make sure you:
// - Install the RsSmw driver package over Packet Manager from Nuget.org
// - Adjust the IP address the match your instrument

using System;
using System.Linq;
using RohdeSchwarz.RsSmw;

namespace RsSmw_ComposeAndLoadWaveform_Example
{
    class Program
    {
        static void Main(string[] args)
        {
            var smw = new RsSmw("TCPIP::10.112.1.179::INSTR", true, true);
            Console.WriteLine("Driver Info: " + smw.Utilities.Identification.DriverVersion);
            Console.WriteLine("Instrument: " + smw.Utilities.Identification.IdnString);
            Console.WriteLine("Instrument options: " + string.Join(",", smw.Utilities.Identification.InstrumentOptions));

            // Creating the I/Q vectors as lists: i_data / q_data
            var pcWvFileA = @"c:\temp\arbFileAexampleCsharp.wv";
            var pcWvFileB = @"c:\temp\arbFileBexampleCsharp.wv";
            var instrWvFileA = @"/var/user/InstrDemoFileA.wv";
            var instrWvFileB = @"/var/user/InstrDemoFileB.wv";
            // Samples clock
            var clockFreq = 100e6;
            // Wave clock
            var waveFreq = 25e6;
            // Scale factor - change it to less or more than 1
            // if you want to see the autoscaling capability of the CreateWaveformFileFromSamples()
            var scaleFactor = 0.8;
            var autoScale = true;
            var step = 1 / clockFreq;
            var count = 200;
            var commentA = "Created from I/Q vectors";
            var commentB = "Created from swapped Q/I vectors";
            var time = Enumerable.Range(0, count).Select(x => step * x);
            // I-component an Q-component data
            var iSamples = time.Select(x => Math.Cos(x * 2 * Math.PI * waveFreq) * scaleFactor).ToList();
            var qSamples = time.Select(x => Math.Sin(x * 2 * Math.PI * waveFreq) * scaleFactor).ToList();

            // Now we have the I / Q vectors, create the pcWvFileA out of them
            smw.ArbFiles.CreateWaveformFileFromSamples(iSamples, qSamples, pcWvFileA, clockFreq, autoScale, commentA);
            // Send the file to the instrument Output A
            smw.ArbFiles.SendWaveformFileToInstrument(pcWvFileA, instrWvFileA);
            // Selecting the waveform and load it in the ARB
            smw.Source.Bb.Arbitrary.Waveform.Select = instrWvFileA;
            smw.Source.Frequency.Fixed.Value = 1.1E9;
            smw.Source.Power.Level.Immediate.Amplitude = -11.1;
            // Turning on the ARB baseband
            smw.Source.Bb.Arbitrary.State = true;
            //  Turning on the RF out state
            smw.Output.State.Value = true;

            // Do the same for the swapped I / Q vectors, create the pcWvFileB out of them
            smw.ArbFiles.CreateWaveformFileFromSamples(qSamples, iSamples, pcWvFileB, clockFreq, autoScale, commentB);

            // Send the file to the instrument Output B
            var smwB = smw.Clone();
            smwB.RepCapHwInstance = HwInstanceRepCap.InstB;
            smwB.ArbFiles.SendWaveformFileToInstrument(pcWvFileB, instrWvFileB);
            // Selecting the waveform and load it in the ARB
            smwB.Source.Bb.Arbitrary.Waveform.Select = instrWvFileB;
            smwB.Source.Frequency.Fixed.Value = 2.2E9;
            smwB.Source.Power.Level.Immediate.Amplitude = -22.2;
            // Turning on the ARB baseband
            smwB.Source.Bb.Arbitrary.State = true;
            //  Turning on the RF out state
            smwB.Output.State.Value = true;

			// Closing the sessions
            smw.Dispose();
            smwB.Dispose();
			
            Console.Write("\n\nPress any key...");
            Console.ReadKey();
        }
    }
}