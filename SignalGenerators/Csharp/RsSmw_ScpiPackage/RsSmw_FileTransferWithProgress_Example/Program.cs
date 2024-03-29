﻿// Example on how to use the read/write handlers to show progress of a big file transfer
// The example does the following:
// - Generates a random file of 20MB
// - Sends this file to the instrument with chunks 1000 000 bytes big
// - After writing each chunk the driver invokes the registered handler which allows for showing the transfer progress
// - The same file is then read back to the instrument
// - After reading each chunk the driver invokes the same handler to show the read transfer progress

// Make sure you:
// - Install the RsSmw driver package over Packet Manager from Nuget.org
// - Adjust the IP address the match your instrument

using System;
using System.IO;
using RohdeSchwarz.RsSmw;

namespace RsSmw_FileTransferWithProgress_Example
{
    class Program
    {
        static void Main()
        {
            int sizeInMb = 20;
            string pcFile = @"c:\temp\randomFile.bin";
            string instrFile = @"/var/user/bigFileInstr.bin";
            string pcFileBack = @"c:\temp\randomFileBack.bin";

            Console.WriteLine("Creating a random file");
            byte[] data = new byte[sizeInMb * 1024 * 1024];
            Random rng = new Random();
            rng.NextBytes(data);
            File.WriteAllBytes(pcFile, data);

            var smw = new RsSmw("TCPIP::10.102.52.47::HISLIP", true, true);
            // Set the one segment after which the handler is called to 1000000 bytes
            smw.Utilities.IoSegmentSize = 1000000;
            Console.WriteLine("Transfer to the instrument started");
            smw.Utilities.Events.WriteSegmentHandler = MyHandler;
            smw.Utilities.File.FromPcToInstrument(pcFile, instrFile);
            smw.Utilities.Events.WriteSegmentHandler = null;
            Console.WriteLine("\nTransfer to the instrument finished\n\n");

            Console.WriteLine("Transfer back from the instrument started");
            smw.Utilities.Events.ReadSegmentHandler = MyHandler;
            smw.Utilities.File.FromInstrumentToPc(instrFile, pcFileBack);
            smw.Utilities.Events.ReadSegmentHandler = null;
            Console.WriteLine("\nTransfer back from the instrument finished\n");
			
			// Closing the session
            smw.Dispose();

            Console.Write("\n\nPress any key...");
            Console.ReadKey();
        }

        public static void MyHandler(object obj, InstrSegmentEventArgs args)
        {
            Console.WriteLine($"Chunk {args.SegmentIx}, transfer {args.TransferredSize} / {args.TotalSize}");
        }
    }
}
