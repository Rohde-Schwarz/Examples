// See https://aka.ms/new-console-template for more information
using System;
using RohdeSchwarz.RsInstrument; // RsInstrument is a Nuget Package, install it through the Nuget Package Manager

// Example for remote-controlling R&S Vector Network Analyzers.
// It shows the following:
// - Sets up Channel 1 and one Trace
// - Sets 3 different markers
// - Performs a single sweep
// - Reads out the sweep data, and save them to the PC as formatted, and complex csv-data
// - Reads out the values of all 3 markers
// - Creates a screenshot and transfers it to the PC as a PNG image file

RsInstrument vna;

try //separate try-catch for initialization prevents accessing uninitialized object
{
    //-----------------------------------------------------------
    //Initialization:
    //-----------------------------------------------------------
    // Adjust the VISA Resource string to fit your instrument
    vna = new RsInstrument("TCPIP::192.168.1.100::hislip0", true, true);
    Console.WriteLine($"Instrument Identification string: \n{vna.Identification.IdnString}");
}
catch (RsInstrumentException e)
{
    Console.WriteLine("Error initializing the instrument session:\n{0}", e.Message);
    Console.WriteLine("Press any key to finish.");
    Console.ReadKey();
    return;
}

vna.VisaTimeout = 3000; // Timeout for VISA Read Operations
vna.OpcTimeout = 15000; // Timeout for opc-synchronised operations

// Configure Channel
vna.Write("SENS1:FREQ:STAR 1000000000");
vna.Write("SENS1:FREQ:STOP 8000000000");
vna.Write("SENS1:SWE:POIN 201");
vna.Write("SENS1:BAND 1000.0 Hz");
vna.Write("SOUR2:POW -10 dBm");
vna.Write("SENS1:SWE:POIN 201");
vna.QueryOpc();

// Configure Trace
vna.Write("CALC1:PAR:MEAS 'Trc1','S21'");
vna.Write("CALC1:FORM MLOG");
vna.QueryOpc();

// Configure Markers
vna.Write("CALC1:PAR:SEL 'Trc1'");
vna.Write("CALC1:MARK1 1");
vna.Write("CALC1:MARK2 1");
vna.Write("CALC1:MARK3 1");
vna.Write("CALC1:MARK1:X 1000000000.0");
vna.Write("CALC1:MARK2:X 2000000000.0");
vna.Write("CALC1:MARK3:X 3000000000.0");
vna.QueryOpc();

// Configure Diagram
vna.Write("DISP:WIND1:TITL:DATA 'S21 Magnitude (dB)'");

// Perform utomatic calibration (optional)
//vna.WriteWithOpc("SENS1:CORR:COLL:AUTO '',2,3", 30000);

// Perform one single sweep
vna.Write("INIT:CONT:ALL OFF");
Console.Write("\nStarting the sweep... ");
vna.Write("INIT:ALL");
// Wait for the sweep to finish before continuing further
vna.QueryOpc();
Console.WriteLine("finished\n");

// Auto-scale display with measured data
vna.Write("DISP:TRAC:Y:AUTO ONCE, 'Trc1'");
vna.QueryOpc();

// Read markers
vna.Write("CALC1:PAR:SEL 'Trc1'");
vna.QueryOpc();

var marker1Name = vna.Query("CALC1:MARK1:NAME?");
var marker1X = vna.QueryDouble("CALC1:MARK1:X?");
var marker1Y = vna.QueryDouble("CALC1:MARK1:Y?");
Console.WriteLine($"Marker 1 {marker1Name}: {marker1X:F2} Hz, {marker1Y:F2} dB");

var marker2Name = vna.Query("CALC1:MARK2:NAME?");
var marker2X = vna.QueryDouble("CALC1:MARK2:X?");
var marker2Y = vna.QueryDouble("CALC1:MARK2:Y?");
Console.WriteLine($"Marker 2 {marker2Name}: {marker2X:F2} Hz, {marker2Y:F2} dB");

var marker3Name = vna.Query("CALC1:MARK3:NAME?");
var marker3X = vna.QueryDouble("CALC1:MARK3:X?");
var marker3Y = vna.QueryDouble("CALC1:MARK3:Y?");
Console.WriteLine($"Marker 3 {marker3Name}: {marker3X:F2} Hz, {marker3Y:F2} dB");

// Save Trace data and transfer them to PC
vna.Write("MMEM:STOR:TRAC 'Trc1', 'Trc1-formatted.csv', FORM, COMP, POIN, COMM");
vna.File.FromInstrumentToPc("Trc1-formatted.csv", @"c:\temp\PC_File_Trc1-formatted.csv");
vna.Write("MMEM:DEL 'Trc1-formatted.csv',FORC");
Console.WriteLine();
Console.WriteLine(@"Formatted Trace 1 saved to c:\temp\PC_File_Trc1-formatted.csv");

vna.Write("MMEM:STOR:TRAC 'Trc1', 'Trc1-complex.csv', UNF, COMP, POIN, COMM");
vna.File.FromInstrumentToPc("Trc1-complex.csv", @"c:\temp\PC_File_Trc1-complex.csv");
vna.Write("MMEM:DEL 'Trc1-complex.csv',FORC");
Console.WriteLine(@"Complex Trace 1 saved to c:\temp\PC_File_Trc1-complex.csv");

// Save Diagram screenshot
vna.Write("DISP:WIND1:MAX 1"); // Select window (active)
vna.Write("MMEM:NAME 'diagram1.png'");
vna.Write("HCOP:DEV:LANG PNG");
vna.Write("HCOP:PAGE:WIND ACT");
vna.Write("HCOP:DEST 'MMEM'");
vna.Write("HCOP");
vna.QueryOpc();
Console.WriteLine(@"Diagram screenshot saved to c:\temp\PC_File_Trc1-complex.csv");
vna.File.FromInstrumentToPc("diagram1.png", @"c:\temp\PC_File_diagram1.png");
vna.Write("MMEM:DEL 'diagram1.png',FORC");

// Close the session
vna.Dispose();

Console.WriteLine("\nPress any key to finish.");
Console.ReadKey();
