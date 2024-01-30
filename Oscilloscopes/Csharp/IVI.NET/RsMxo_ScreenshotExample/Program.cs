using System;
using Ivi.Driver;
using Ivi.Scope;

// To use the namespace RohdeSchwarz.RsMxo, add the reference to the last version of the RohdeSchwarz.RsMxo.Fx40 assembly
// with ProjectItem 'References'->RightClick->AddReference->Search 'rsmxo'
// If not found, add them from here (AnyCpu): 
// "c:\Program Files\IVI Foundation\IVI\Microsoft.NET\Framework64\v4.0.30319\RohdeSchwarz.RsMxo 1.2.0\RohdeSchwarz.RsMxo.Fx40.dll"
using RohdeSchwarz.RsMxo;

//--------------------------------------------------------------------------
// Prerequisites
//
//   This sample program needs IVI Shared Components and IVI.NET Shared Components being installed.
//   To download them, go to http://www.ivifoundation.org/shared_components/Default.aspx
//
//   Download and install
//     - IVI Shared Components 3.0.0 or newer
//     - IVI.NET Shared Components 2.0.0 or newer
//     - Rohde & Schwarz RsMxo IVI.NET driver 1.2.0 or newer
//
//--------------------------------------------------------------------------

namespace ScreenshotExample
{
    static class Program
    {
        [STAThread]
        static void Main()
        {
            bool reset = false;
            string instrSrcFile = "/home/instrument/userData/screenshots/Print.png";
            string pcTargetFile = "c:/temp/_screenshot_mxo.png";
            var mxo = new RsMxo("TCPIP::10.205.0.159::hislip0", false, reset);
                       
            mxo.Settings.System.Remote.DisplayUpdateEnabled = true;

            mxo.SaveRecall.Screenshot.IncludeSignalBar = false;
            mxo.SaveRecall.Screenshot.ShowSetupDialog = true;
            mxo.SaveRecall.Screenshot.WhiteBackground = true;
            mxo.SaveRecall.Screenshot.InvertColor = true;
            mxo.SaveRecall.Screenshot.FileExtension = ScreenshotFileFormat.Png;

            Console.Write("\nCreating the screenshot ...");
            mxo.SaveRecall.Screenshot.Save();
            Console.WriteLine(" done");

            mxo.SaveRecall.FileManagment.ReadToFileFromInstrument(instrSrcFile, pcTargetFile);
            Console.WriteLine("\n\nScreeenshot copied to : " + pcTargetFile);
            mxo.Close();

            Console.Write("\n\nPress any key to finish ... ");
            Console.ReadKey();
        }
    }
}
