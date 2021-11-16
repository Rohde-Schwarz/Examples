// RsNgx example showing how to make a screenshot of the instrument display

using System;
using System.IO;
using RohdeSchwarz.RsNgx;

namespace RsNgx_Example
{
    class Program
    {
        static void Main()
        {
            var filePath = @"c:\temp\ngx_screenshot.png";
                
            var ngx = new RsNgx("TCPIP::10.102.52.45::INSTR", true, false);
            //var ngx = new RsNgx("TCPIP::10.102.52.45::INSTR", true, true, "SelectVisa=RsVisa"); // Forcing R&S VISA
            //var ngx = new RsNgx("TCPIP::10.102.52.45::5025::SOCKET", true, true, "SelectVisa=SocketIo"); // No VISA needed
            Console.WriteLine("Hello, I am: " + ngx.Utilities.Identification.IdnString);

            // Driver's instrument status checking ( SYST:ERR? ) after each command (default value is true):
            ngx.Utilities.InstrumentStatusChecking = true;
            ngx.Utilities.Reset();

            ngx.Display.Window.Text.Data = "My Greetings to you ...";
            ngx.HardCopy.Format.Set(HcpyFormatEnum.PNG);
            var picture = ngx.HardCopy.Data;
            File.WriteAllBytes(filePath, picture);
            Console.WriteLine($"\nScreenshot saved to {filePath}");

            // Closing the session
            ngx.Dispose();

            Console.Write("\n\nPress any key...");
            Console.ReadKey();
        }
    }
}
