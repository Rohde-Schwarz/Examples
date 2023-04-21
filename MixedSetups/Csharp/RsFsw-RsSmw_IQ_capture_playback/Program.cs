/*
This C# example captures IQ data from FSW Signal Analyzer,
creates an IQ waveform file (.wv format) and sends it to SMW Vector Signal Generator (ARB mode).

Tested with:
- R&S VISA 5.12.8
- RsFsw 5.20.2.84
- RsSmw 5.0.170.97
- FSW - FW: 5.21
- SMW - FW: 5.10.035.29

Preconditions:
- RsFsw 5.20.2.84 or higher
- RsSmw 5.0.170.97 or higher

Author: R&S Customer Support - MP
Last Update: 21.04.2023
Version: v1.2

Technical support -> www.rohde-schwarz.com/support

Before running, please always check this script for unsuitable setting !
This example does not claim to be complete. All information have been
compiled with care. However, errors can’t be ruled out.
*/

using System;
using System.Linq;
using System.Collections.Generic;
using System.Threading.Tasks;
using System.Diagnostics;
using RohdeSchwarz.RsFsw;
using RohdeSchwarz.RsSmw;

namespace RsFsw_RsSmw_IQ_capture_playback
{
    class Program
    {
        static void Main(string[] args)
        {
            // *** user controls ***
            bool socketConnection = false; // does not require VISA library if set to true, HiSLIP protocol used if set to false
            int socketTimeout = 30000; // for connection type 'Socket' only -> send / receive timeout = VISA timeout

            // Signal Analyzer
            string fswIp = "10.205.0.30";
            bool fswReset = true;
            double fswCenterFreq = 1.5e9;
            double fswRefLevel = -8;
            double fswIqBw = 98.304e6;
            double fswAcqTime = 20e-3;
            var fswTrgSrc = TriggerSeqSourceEnum.IMMediate;

            // Vector Signal Generator
            string smwIp = "10.205.0.138";
            bool smwReset = true;
            string wvFilename = "arbFile.wv";
            string wvFilePathPc = @"c:\temp\" + wvFilename;
            string wvFilePathInstr = @"/var/user/" + wvFilename;
            string wvFileComment = "FSW IQ data";
            double smwRfFreq = fswCenterFreq;
            double smwPwrLevel = -20;
            // *** user controls end ***

            string fswRsc = "TCPIP::" + fswIp + "::HISLIP";
            string smwRsc = "TCPIP::" + smwIp + "::HISLIP";
            string selectVisa = "SelectVisa=RsVisa";

            if (socketConnection == true)
            {
                fswRsc = "TCPIP::" + fswIp + "::5025::SOCKET";
                smwRsc = "TCPIP::" + smwIp + "::5025::SOCKET";
                selectVisa = "SelectVisa=SocketIo";
            }

            // Connect to instruments in parallel processes
            Console.WriteLine("\nConnect to instruments ...");
            RsFsw fsw = null;
            RsSmw smw = null;
            Parallel.Invoke(() =>
            {
                fsw = new RsFsw(fswRsc, false, fswReset, selectVisa); // connect to FSW
            }
            , () =>
            {
                smw = new RsSmw(smwRsc, false, smwReset, selectVisa); // connect to SMW
            });

            Console.WriteLine("Instrument: " + fsw.Utilities.Identification.IdnString);
            Console.WriteLine("Driver Info : " + fsw.Utilities.Identification.DriverVersion);
            //Console.WriteLine("Instrument options: " + string.Join(",", fsw.Utilities.Identification.InstrumentOptions));
            fsw.Utilities.InstrumentStatusChecking = true;
            fsw.Utilities.OpcQueryAfterEachSetting = false;
            fsw.System.Display.Update.Set(true);

            Console.WriteLine("Instrument: " + smw.Utilities.Identification.IdnString);
            Console.WriteLine("Driver Info: " + smw.Utilities.Identification.DriverVersion);
            //Console.WriteLine("Instrument options: " + string.Join(",", smw.Utilities.Identification.InstrumentOptions));
            smw.Utilities.InstrumentStatusChecking = true;
            smw.Utilities.OpcQueryAfterEachSetting = false;

            // get IQ data from FSW
            fsw.Instrument.Create.New.Set(ChannelTypeEnum.IqAnalyzer, "IQ Analyzer");
            fsw.Applications.IqAnalyzer.Trace.Iq.Data.Format.Set(IqResultDataFormatEnum.IQBLock);
            fsw.Format.Data.Set(DataFormatEnum.Real32);
            fsw.Sense.Frequency.Center.Set(fswCenterFreq);
            fsw.Display.Window.Trace.Y.Scale.RefLevel.Set(fswRefLevel);
            fsw.Trace.Iq.Bandwidth.Set(fswIqBw);
            fsw.Sense.Sweep.Time.Set(fswAcqTime);
            fsw.Trigger.Sequence.Source.Set(fswTrgSrc);
            fsw.Utilities.QueryOpc();

            fsw.Initiate.Continuous.Set(false);
            var fswSampleRate = fsw.Applications.IqAnalyzer.Trace.Iq.SymbolRate.Get();
            var fswRecLength = fsw.Applications.IqAnalyzer.Trace.Iq.Rlength.Get();
            Console.WriteLine("\nfswSampleRate: " + fswSampleRate/1e6 + " MHz");
            Console.WriteLine("fswRecLength: " + fswRecLength + " IQ Samples");

            Console.WriteLine("\nFetch IQ data from Signal Analyzer ...");
            Stopwatch stopwatch = new Stopwatch();
            stopwatch.Start();
            fsw.Initiate.ImmediateAndWait();
            var iqSamples = fsw.Trace.Iq.Data.MemoryAll.Get();
            stopwatch.Stop();
            TimeSpan stopwatchElapsed = stopwatch.Elapsed;
            Console.WriteLine("done - time elapsed: " + Convert.ToInt32(stopwatchElapsed.TotalMilliseconds) + "ms");

            Console.WriteLine("\nDisconnect from Signal Analyzer ...");
            fsw.Utilities.GoToLocal();
            fsw.Dispose(); // disconnect from FSW

            // normalize IQ data
            var iSamples = iqSamples.Take(fswRecLength).ToList();
            var qSamples = iqSamples.Skip(fswRecLength).Take(fswRecLength).ToList();

            var normRef = Math.Sqrt(Math.Pow(10, (fswRefLevel / 10)) * 1e-3 * 50);

            var iSamplesNorm = new List<double>();
            var qSamplesNorm = new List<double>();
            var iqMagNorm = new List<double>(new double[iSamples.Count]);

            for (int i = 0; i < iSamples.Count; i++)
            {
                iSamplesNorm.Add(iSamples[i] / normRef);
                qSamplesNorm.Add(qSamples[i] / normRef);
                iqMagNorm[i] = Math.Sqrt(Math.Pow(iSamplesNorm[i], 2) + Math.Pow(qSamplesNorm[i], 2));
            }

            // create waveform file
            Console.WriteLine("\nCreate waveform file ...");
            stopwatch.Reset();
            stopwatch.Start();
            RsSmw_ArbFiles.CreateWaveformFileFromSamples(iSamplesNorm, qSamplesNorm, wvFilePathPc, fswSampleRate, true, wvFileComment);
            stopwatch.Stop();
            stopwatchElapsed = stopwatch.Elapsed;
            Console.WriteLine("done - time elapsed: " + Convert.ToInt32(stopwatchElapsed.TotalMilliseconds) + "ms");

            // send waveform file to SMW
            Console.WriteLine("\nSend waveform file to VSG ...");
            stopwatch.Reset();
            stopwatch.Start();
            int smwVisaTimeoutDefault = smw.Utilities.VisaTimeout;
            if (selectVisa == "SelectVisa=SocketIo") smw.Utilities.VisaTimeout = socketTimeout;
            smw.ArbFiles.SendWaveformFileToInstrument(wvFilePathPc, wvFilePathInstr);
            smw.Utilities.VisaTimeout = smwVisaTimeoutDefault;
            stopwatch.Stop();
            stopwatchElapsed = stopwatch.Elapsed;
            Console.WriteLine("done - time elapsed: " + Convert.ToInt32(stopwatchElapsed.TotalMilliseconds) + "ms");

            // play waveform file
            Console.WriteLine("\nPlay waveform file ...");
            stopwatch.Reset();
            stopwatch.Start();
            smw.Source.Bb.Arbitrary.Waveform.Select = wvFilePathInstr;
            smw.Utilities.QueryOpc();
            smw.Source.Bb.Arbitrary.State = true;
            smw.Utilities.QueryOpc();
            stopwatch.Stop();
            stopwatchElapsed = stopwatch.Elapsed;
            Console.WriteLine("done - time elapsed: " + Convert.ToInt32(stopwatchElapsed.TotalMilliseconds) + "ms");

            // output RF signal
            smw.Source.Frequency.Fixed.Value = smwRfFreq;
            smw.Source.Power.Level.Immediate.Amplitude = smwPwrLevel;
            smw.Output.State.Value = true;

            Console.WriteLine("\nDisconnect from Vector Signal Generator ...");
            smw.Dispose(); // disconnect from SMW

            Console.Write("\nPress any key to exit ");
            Console.ReadKey();
        }
    }
}
