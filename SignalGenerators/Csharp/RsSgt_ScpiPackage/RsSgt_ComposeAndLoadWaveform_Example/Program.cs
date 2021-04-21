// Example of creating Rohde Schwarz Waveform file, sending it to the instrument and activating it
// The example does the following:
// - Generates I/Q vectors iSamples and qSamples
// - Creates a waveform file out of them: pcWvFile
// - Sends it to the instrument
// - Activates the Arbitrary generator
// - Sets the RF Output

// Make sure you:
// - Install the RsSgt driver package over Packet Manager from Nuget.org
// - Adjust the IP address the match your instrument

using System;
using System.Linq;
using RohdeSchwarz.RsSgt;

namespace RsSgt_ComposeAndLoadWaveform_Example
{
    class Program
    {
        static void Main(string[] args)
        {
            var sgt = new RsSgt("TCPIP::10.112.1.73::INSTR", true, true);
            Console.WriteLine("Driver Info: " + sgt.Utilities.Identification.DriverVersion);
            Console.WriteLine("Instrument: " + sgt.Utilities.Identification.IdnString);
            Console.WriteLine("Instrument options: " + string.Join(",", sgt.Utilities.Identification.InstrumentOptions));

            // Creating the I/Q vectors as lists: i_data / q_data
            var pcWvFile = @"c:\temp\arbFileExampleCsharp.wv";
            var instrWvFile = @"/var/user/InstrDemoFile.wv";
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
            var comment = "Created from I/Q vectors";
            var time = Enumerable.Range(0, count).Select(x => step * x);
            // I-component an Q-component data
            var iSamples = time.Select(x => Math.Cos(x * 2 * Math.PI * waveFreq) * scaleFactor).ToList();
            var qSamples = time.Select(x => Math.Sin(x * 2 * Math.PI * waveFreq) * scaleFactor).ToList();
            
			// Now we have the I / Q vectors, create the pcWvFile out of them
			sgt.ArbFiles.CreateWaveformFileFromSamples(iSamples, qSamples, pcWvFile, clockFreq, autoScale, comment);
            
			// Send the file to the instrument
			sgt.ArbFiles.SendWaveformFileToInstrument(pcWvFile, instrWvFile);
            // Selecting the waveform and load it in the ARB
            sgt.Source.Bb.Arbitrary.Waveform.Select = instrWvFile;
            sgt.Source.Frequency.Fixed.Value = 1.1E9;
            sgt.Source.Power.Level.Immediate.Amplitude = -11.1;
            // Turning on the ARB baseband
            sgt.Source.Bb.Arbitrary.State = true;
            //  Turning on the RF out state
            sgt.Output.State.Value = true;

            // Closing the session
            sgt.Dispose();

            Console.Write("\n\nPress any key...");
            Console.ReadKey();
        }
    }
}