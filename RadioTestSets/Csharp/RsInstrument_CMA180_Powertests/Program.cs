using RohdeSchwarz.RsInstrument; // Nuget Package, install it through the Nuget Package Manager


var cma = new RsInstrument("TCPIP::192.168.1.110::hislip0", false, false);

Console.WriteLine("Hello, I am " + cma.Identification.IdnString);

// Preparation
cma.WriteWithOpc("SYSTem:DISPlay:UPDate ON"); // Be sure the display is not switched off in remote mode
cma.WriteWithOpc("CONFigure:BASE:SCENario EXPert"); // Switch to Expert Mode
cma.Write("SOURce:AFRF:GEN:RFSettings:CONNector RFCom"); // Have the generator output switched to the RF COM port
cma.Write("CONFigure:AFRF:MEAS:RFSettings:CONNector RFCom"); // Also switch the Analyzer input to the RF COM port
cma.Write("SOURce:AFRF:GEN:RFSettings:FREQuency 145 MHz"); // Change generator frequency to 145 MHz
cma.Write("SOURce:AFRF:GEN:RFSettings:LEVel -20"); // Set the (calculated) output level to -20 dBm
// --> will lead to something like 20 dBm detected due to the attenuator being factored in
cma.Write("SOURce:AFRF:GEN:MSCHeme AM"); // Modulation Scheme --> AM
cma.Write("SOURce:AFRF:GEN:MODulator GEN3"); // Enable GEN3 as modulator (will be single tone / 1 kHz as standard after reset)
cma.Write("SOURce:AFRF:GEN:MODulator:MDEPth 80"); // Set mod depth to 80 %
cma.WriteWithOpc("SOURce:AFRF:GEN:STATe ON"); // Start signal transmission

// Signal searching routine using the analyzer's "Find RF" routine
cma.WriteWithOpc("CONFigure:AFRF:MEAS:FREQuency:COUNter:AUTomatic ON"); // Automatically switch analyzer to the detected frequency
cma.WriteWithOpc("INITiate:AFRF:MEAS:FREQuency:COUNter"); // Start to find the signal (should be 145.000 MHz now)
var freqs = cma.Binary.QueryBinOrAsciiFloatArray("FETCh:AFRF:MEAS:FREQuency:COUNter?"); // Get frequency information

Console.WriteLine($"\nFound signal at {freqs[0] / 1E6} MHz");

// First Part: Perform the AM signal measurement
cma.WriteWithOpc("INITiate:GPRF:MEAS:POWer"); // Initiate power measurement
var avAm = cma.Binary.QueryBinOrAsciiFloatArray("FETCh:GPRF:MEAS:POWer:CURRent?")[1]; // Request Average Power, we get two values back

Console.WriteLine($"\nThe AM average power now is {avAm} dBm");
var pkAm = cma.Binary.QueryBinOrAsciiFloatArray("FETCh:GPRF:MEAS:POWer:MAXimum:CURRent?")[1]; // Request Peak Power, we get two values back
Console.WriteLine($"The AM peak power now is {pkAm} dBm");

// Second Part: Perform the CW signal measurement (Power measurement ist still active)
cma.WriteWithOpc("SOURce:AFRF:GEN:MSCHeme CW"); // Modulation Scheme --> CW
cma.WriteWithOpc("INITiate:GPRF:MEAS:POWer"); // Initiate power measurement
var avCw = cma.Binary.QueryBinOrAsciiFloatArray("FETCh:GPRF:MEAS:POWer:CURRent?")[1]; // Request Average Power
Console.WriteLine($"The CW average power now is {avCw} dBm");

// Third Part: Compare Am to CW measurements
// The difference between CW and AM (@ 80% modulation depth) should be:
// 1.2 dB for average and 5,1 dB for peak
// (Conversion rate peak power AM vs CW = 10 * log ((1+m)*(1+m)) = 5.1 dB @ 80 % )
// (Conversion rate RMS power AM vs CW = 10 * log (1+m*m/2) = 1.2 dB @ 80 % )
// 
var diffAmAvCw = avAm - avCw; // Calculate Difference between AM average and CW Power
Console.WriteLine($"Difference between CW and AM average is {diffAmAvCw:F3} dB and should be about 1.2 dB");


var diffAmPkCw = pkAm - avCw;  // Calculate Difference between AM peak and CW power
Console.WriteLine($"\nDifference between CW and AM peak is {diffAmPkCw} dB and should be about 5.1 dB");
