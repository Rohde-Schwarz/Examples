// Getting started - how to work with rsrtx Python package.
// This example performs the following actions on an RTO Oscilloscope:
// - Basic configuration
// - Triggers an acquisition and waits for it to finish.
// - Fetches the waveforms for channel 1 and paints it into a plot.

// The example also shows the corresponding SCPI commands next to the rsrtx calls.
// Notice that the python rsrtx interfaces track the SCPI commands structure.
// Additionally, the SCPI communication logger into the console shows you the SCPI communication with your RTO.

using RohdeSchwarz.RsRtx;


var rto = new RsRtx("TCPIP::10.103.34.49::hislip0");
Console.WriteLine("Hello, I am: " + rto.Utilities.Identification.IdnString);
rto.Trigger.Mode.Set(TriggerModeEnum.AUTO);
rto.Channel.Range.Set(10.0);
rto.Channel.State.Set(true);
Console.Write("\nStarting the acquisition ...");
rto.Run.SingleAndWait();
Console.WriteLine(" acquisition complete");
var header = rto.Channel.Waveform.Data.Header.Get();
Console.WriteLine("Waveform:");
Console.WriteLine($"Time start: {header.Start} s, Time stop: {header.Stop} s");
var waveform = rto.Channel.Waveform.Data.Values.Get();
Console.WriteLine($"Record length: {waveform.Count} samples");

rto.Dispose();
