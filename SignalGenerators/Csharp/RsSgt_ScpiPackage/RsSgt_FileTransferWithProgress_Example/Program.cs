// Example on how to use the read/write handlers to show progress of a big file transfer
// The example does the following:
// - Generates a random file of 20MB
// - Sends this file to the instrument with chunks 1000 000 bytes big
// - After writing each chunk the driver invokes the registered handler which allows for showing the transfer progress
// - The same file is then read back to the instrument
// - After reading each chunk the driver invokes the same handler to show the read transfer progress

// Make sure you:
// - Install the RsSgt driver package over Packet Manager from Nuget.org
// - Adjust the IP address the match your instrument

using System;
using System.IO;
using RohdeSchwarz.RsSgt;

namespace RsSgt_FileTransferWithProgress_Example
{
    class Program
    {
        static void Main(string[] args)
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

            var sgt = new RsSgt("TCPIP::10.112.1.73::INSTR");
            // Set the one segment after which the handler is called to 1000000 bytes
            sgt.Utilities.IoSegmentSize = 1000000;
            Console.WriteLine("Transfer to the instrument started");
            sgt.Utilities.Events.WriteSegmentHandler = MyHandler;
            sgt.Utilities.File.FromPcToInstrument(pcFile, instrFile);
            sgt.Utilities.Events.WriteSegmentHandler = null;
            Console.WriteLine("\nTransfer to the instrument finished\n\n");

            Console.WriteLine("Transfer back from the instrument started");
            sgt.Utilities.Events.ReadSegmentHandler = MyHandler;
            sgt.Utilities.File.FromInstrumentToPc(instrFile, pcFileBack);
            sgt.Utilities.Events.ReadSegmentHandler = null;
            Console.WriteLine("\nTransfer back from the instrument finished\n");

            // Closing the session
            sgt.Dispose();

            Console.Write("\n\nPress any key...");
            Console.ReadKey();
        }

        public static void MyHandler(object obj, InstrSegmentEventArgs args)
        {
            Console.WriteLine($"Chunk {args.SegmentIx}, transfer {args.TransferredSize} / {args.TotalSize}");
        }
    }
}
