using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading.Tasks;

using RohdeSchwarz.RsOsp;

namespace OspCommunicationSample
{
  class Program
  {
    static void Main(string[] args)
    {
      Console.WriteLine("OSP Communication Sample:\r\n");

      OspCommunication();

      Console.Write("\r\n\r\nPress ENTER to end OSP Communication Sample Tool.\r\n");
      Console.ReadLine();
    }

    static void OspCommunication()
    {
      // get IP address of OSP
      Console.Write("Enter IP address of OSP: ");
      string ipAddress = Console.ReadLine();
      Console.WriteLine();

      // Resource name of OSP for VISA session
      string resourceName = "TCPIP::" + ipAddress + "::INSTR";

      // flag to check if device is OSP when starting VISA session
      bool idQuery = true;

      // flag to request a device reset when starting VISA session
      bool resetDevice = false;

      // string for optional settings of VISA session, i.e. VISA timeout value
      string optionString = "VisaTimeout = 5000";

      try
      {
        // start VISA session
        RsOsp osp = new RsOsp(resourceName, idQuery, resetDevice, optionString);

        if (osp != null)
        {
          Console.WriteLine("----------------------------------------------------------------------------------------------");
          Console.WriteLine("O S P    D E V I C E    I N F O R M A T I O N :");
          Console.WriteLine("----------------------------------------------------------------------------------------------\r\n");

          // string returned by *IDN?
          Console.WriteLine("Identification ............ = " + osp.Utilities.Identification.IdnString + "\r\n");

          // single device information
          Console.WriteLine("Instrument Manufacturer ... = " + osp.Utilities.Identification.Manufacturer);
          Console.WriteLine("Instrument Name ........... = " + osp.Utilities.Identification.InstrumentName);
          Console.WriteLine("Instrument Serial Number .. = " + osp.Utilities.Identification.InstrumentSerialNumber);
          Console.WriteLine("Instrument Firmware Version = " + osp.Utilities.Identification.InstrumentFirmwareVersion + "\r\n");

          // some other useful information
          Console.WriteLine("Session Resource Name ..... = " + osp.Utilities.Identification.ResourceName);
          Console.WriteLine("VISA Timeout .............. = " + osp.Utilities.VisaTimeout + " ms");
          Console.WriteLine("VISA Manufacturer ......... = " + osp.Utilities.Identification.VisaManufacturer);
          Console.WriteLine("Driver Version ............ = " + osp.Utilities.Identification.DriverVersion + "\r\n");

          string locationB101 = string.Empty;
          string locationB102 = string.Empty;
          string locationB103 = string.Empty;
          int numberOfControlledModules = 0;

          // get list of installed hardware
          var modules = osp.Diagnostic.Service.HwInfo;
          var numModules = modules.Count();
          Console.WriteLine("\r\nIdentified Hardware: " + numModules + "\r\n");
          foreach (string module in modules)
          {
            var info = module.Split('|');
            Console.WriteLine("   Location ....... = " + info[0]);
            Console.WriteLine("   Name ........... = " + info[1]);
            Console.WriteLine("   Serial Number .. = " + info[2]);
            Console.WriteLine("   Part Number .... = " + info[3]);
            Console.WriteLine("   Hardware Code .. = " + info[4]);
            Console.WriteLine("   Product Index .. = " + info[5] + "\r\n");

            // check for OSP-B101
            if (info[1] == "OSP-B101")
            {
              locationB101 = info[0];
              numberOfControlledModules++;
            }

            // check for OSP-B102
            if (info[1] == "OSP-B102")
            {
              locationB102 = info[0];
              numberOfControlledModules++;
            }

            // check for OSP-B103
            if (info[1] == "OSP-B103")
            {
              locationB103 = info[0];
              numberOfControlledModules++;
            }
          }


          // get list of controlled frames
          var devices = osp.Configure.Frame.Catalog;
          var numDevices = devices.Count;
          Console.WriteLine("\r\nDefined Frames: " + numDevices + "\r\n");
          foreach (string device in devices)
          {
            if (!string.IsNullOrEmpty(device))
            {
              Console.WriteLine("   Frame Definition:  " + device + "\r\n");
            }
          }

          // get list of path definitions
          var paths = osp.Route.Path.Catalog;
          var numPaths = paths.Count;
          Console.WriteLine("\r\nDefined Path Definitions: " + numPaths + "\r\n");
          foreach (string path in paths)
          {
            if (!string.IsNullOrEmpty(path))
            {
              Console.WriteLine("   Path Name:  " + path);

              // get path definition
              var pathDefinition = osp.Route.Path.Define.Get(path);
              Console.WriteLine(pathDefinition);
              Console.WriteLine();
            }
          }

          Console.WriteLine("\r\nModule Operations: " + numberOfControlledModules +"\r\n");

          // control module OSP-B101
          if (!string.IsNullOrEmpty(locationB101))
          {
            Console.WriteLine("OSP-B101 is located at " + locationB101 + ":\r\n");

            var channelInfo = "(@" + locationB101 + "(0111))";
            Console.WriteLine("   Switching relay K11 to position 1");
            osp.Route.Close.Set(channelInfo);
            var responseList = osp.Route.Close.Get(channelInfo);
            Console.WriteLine("   Checking position 1 of relay K11: " + (responseList[0] == false ? "false" : "true"));

            channelInfo = "(@" + locationB101 + "(0112:0116))";
            Console.WriteLine("   Switching relay K12..K16  to position 1");
            osp.Route.Close.Set(channelInfo);
            responseList = osp.Route.Close.Get(channelInfo);
            Console.WriteLine("   Checking position 1 of relay K11..K16: " + (responseList.Contains(false) ? "false" : "true"));
            Console.WriteLine();
          }

          // control module OSP-B102
          if (!string.IsNullOrEmpty(locationB102))
          {
            Console.WriteLine("OSP-B102 is located at " + locationB102 + ":\r\n");

            var channelInfo = "(@" + locationB102 + "(0602))";
            Console.WriteLine("   Switching relay K2 to position 6");
            osp.Route.Close.Set(channelInfo);
            var responseList = osp.Route.Close.Get(channelInfo);
            Console.WriteLine("   Checking position 6 of relay K2: " + (responseList[0] == false ? "false" : "true"));

            channelInfo = "(@" + locationB102 + "(0401:0402))";
            Console.WriteLine("   Switching relay K1..K2  to position 4");
            osp.Route.Close.Set(channelInfo);
            responseList = osp.Route.Close.Get(channelInfo);
            Console.WriteLine("   Checking position 4 of relay K1..K2: " + (responseList.Contains(false) ? "false" : "true"));
            Console.WriteLine();
          }

          // control module OSP-B103
          if (!string.IsNullOrEmpty(locationB103))
          {
            Console.WriteLine("OSP-B103 is located at " + locationB103 + ":\r\n");

            var channelInfo = "(@" + locationB103 + "(0102))";
            Console.WriteLine("   Switching output CH2 to position 1");
            osp.Route.Close.Set(channelInfo);
            var responseList = osp.Route.Close.Get(channelInfo);
            Console.WriteLine("   Checking position 1 of output CH2: " + (responseList[0] == false ? "false" : "true"));

            channelInfo = "(@" + locationB103 + "(0109:0116))";
            Console.WriteLine("   Switching output CH9..CH16 to position 1");
            osp.Route.Close.Set(channelInfo);
            responseList = osp.Route.Close.Get(channelInfo);
            Console.WriteLine("   Checking position 1 of output CH9..CH16: " + (responseList.Contains(false) ? "false" : "true"));

            channelInfo = "(@" + locationB103 + ")";
            var inputList = osp.Read.Io.Input.Get(channelInfo);
            Console.WriteLine("   Reading inputs: 0x" + Convert.ToString(inputList[0], 16) + "\r\n");
            for (int input = 0; input < 16; input++)
            {
              Console.WriteLine("      IN" + (input + 1).ToString("00") + " = " + (((0x01 << input) & inputList[0]) > 0 ? "1" : "0"));
            }
            Console.WriteLine();
          }

          // reset OSP
          Console.WriteLine("\r\nResetting all switches.\r\n\r\n");
          osp.Utilities.Reset();

          // check for errors
          var errors = osp.Utilities.QueryAllErrors();

          // list all errors
          if (errors.Any())
          {
            Console.WriteLine("System Errors: " + errors.Count() + "\r\n");
            foreach (string error in errors)
            {
              Console.WriteLine(error);
            }
          }
          else
          {
            Console.WriteLine("No System Errors!");
          }

        }

        // end VISA session
        osp.Dispose();
      }
      catch(Exception ex)
      {
        Console.WriteLine("EXCEPTION caught:\r\n" + ex.Message + "\r\n");
      }
    }
  }
}
