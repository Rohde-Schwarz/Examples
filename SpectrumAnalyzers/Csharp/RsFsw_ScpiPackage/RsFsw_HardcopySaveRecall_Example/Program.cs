// RsFsw Python package example. Performs the following:
// Creates new FSW application.
// Takes a screenshot and transfers the file to the control PC.
// Saves the instrument status to a file 'RsFswState.dfl'.
// Copies the 'RsFswState.dfl' file under a different name to the PC: 'RsFswState_PC.dfl'
// Copies the file 'RsFswState_PC.dfl' back to the instrument under a new name 'RsFswState_back.dfl'.
//   This simulates acquiring and distribution of a setup file from the Control PC.
// Resets the instrument
// Recalls the status from the 'RsFswState_back.dfl'

// Preconditions:
// - Install the RsFsw driver package over Packet Manager from NuGet.org
// - Adjust the IP address the match your instrument

using System;
using RohdeSchwarz.RsFsw;

namespace RsFsw_HardcopySaveRecall_Example
{
    class Program
    {
        static void Main(string[] args)
        {
            var fsw = new RsFsw("TCPIP::192.168.1.102::HISLIP", true, true);
            //var fsw = new RsFsw("TCPIP::192.168.1.102::INSTR", true, true, "SelectVisa=RsVisa"); // Forcing R&S VISA
            //var fsw = new RsFsw("TCPIP::192.168.1.102::5025::SOCKET", true, true, "SelectVisa=SocketIo"); // No VISA installation needed
            Console.WriteLine("Instrument: " + fsw.Utilities.Identification.IdnString);

            // Driver's instrument status checking ( SYST:ERR? ) after each command (default value is true):
            fsw.Utilities.InstrumentStatusChecking = true;

            //  SYSTem:DISPlay:UPDate ON
            fsw.System.Display.Update.Set(true);

            // Create new instrument PhaseNoise
            fsw.Instrument.Create.New.Set(ChannelTypeEnum.K40_PhaseNoise, "NoiseOnly");

            // Add new window with SpotNoiseTable results at the bottom
            var newName = fsw.Applications.K40_PhaseNoise.Layout.Add.Window.Get("2", WindowDirectionEnum.BELow, WindowTypeK40enum.SpotNoiseTable);

            // Let's make a screenshot
            fsw.HardCopy.Mode.Set(HardcopyModeEnum.SCReen);
            fsw.HardCopy.Device.Color.Set(true);
            // Set the color map. Colors.Ix4 means: Screen colors without changes
            fsw.HardCopy.Cmap.Default.Set(ItemRepCap.Ix1, ColorsRepCap.Ix4);
            fsw.MassMemory.Name.Set(@"c:\Temp\Device_Screenshot2.png");
            fsw.HardCopy.Immediate.SetAndWait();
            // Copy the screenshot to the PC
            fsw.Utilities.File.FromInstrumentToPc(@"c:\Temp\Device_Screenshot2.png", @"c:\Temp\PC_Screenshot2.png");
            Console.WriteLine(@"Screenshot saved here: c:\Temp\PC_Screenshot2.png");

            // Save the current instrument status to a recall file
            fsw.MassMemory.Store.State.Set(@"RsFswState.dfl");
            // Copy the setup file to the PC under a different name
            fsw.Utilities.File.FromInstrumentToPc(@"RsFswState.dfl", @"c:\Temp\RsFswState_PC.dfl");
            Console.WriteLine(@"Setup file saved here: c:\Temp\RsFswState_PC.dfl");
            // Copy the setup file back to the instrument as 'RsFswState_back.dfl'
            fsw.Utilities.File.FromPcToInstrument(@"c:\Temp\RsFswState_PC.dfl", @"RsFswState_back.dfl");

            // Make a reset and restore the saved state.
            fsw.Utilities.Reset();

            // Restore the instrument status with the file copied back from the PC
            fsw.MassMemory.Load.State.Set(@"RsFswState_back.dfl");

            // Close the session
            fsw.Dispose();

            Console.WriteLine("\nPress any key");
            Console.ReadKey();
        }
    }
}
