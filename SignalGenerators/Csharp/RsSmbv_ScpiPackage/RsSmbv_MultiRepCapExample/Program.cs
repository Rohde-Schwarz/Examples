// Example to demonstrate how to work with commands that have many repeated capabilities (numeric suffixes).
// The example does not perform any valid instrument settings,
// rather the driver's general rules of working with the repeated capabilities.

// Make sure you:
// - Install the RsSmw driver package over Packet Manager from Nuget.org
// - Adjust the IP address the match your instrument

using System;
using RohdeSchwarz.RsSmbv;

namespace RsSmw_Example
{
    class Program
    {
        static void Main()
        {
            var smbv = new RsSmbv("TCPIP::10.112.1.67::INSTR", true, true);
            Console.WriteLine("Driver Info: " + smbv.Utilities.Identification.DriverVersion);
            Console.WriteLine("Instrument: " + smbv.Utilities.Identification.IdnString);

            // Switching the error checking off to avoid errors from invalid parameter settings
            smbv.Utilities.InstrumentStatusChecking = false;

            // The driver object uses the global HW instance one - RF out A
            smbv.RepCapHwInstance = HwInstanceRepCap.InstA;

            smbv.Source.Bb.Nr5G.State = true;

            // Setting commands with many repeated capabilities:
            // [SOURce<HW>]:BB:NR5G:SCHed:CELL<CH>:SUBF<ST>:USER<US>:BWPart<BWP>:ALLoc<ALC>:APMap:COL<S2US>:ROW<S3US>:IMAGinary
            // Option 1: explicit definition:
            // Sending SOURce1:BB:NR5G:SCHed:CELL1:SUBF3:USER0:BWPart1:ALLoc0:APMap:COL2:ROW3:IMAGinary 10.0
            smbv.Source.Bb.Nr5G.Scheduling.Cell.Subf.User.BwPart.Alloc.ApMap.Col.Row.Imaginary.Set(
                10.0,
                CellNullRepCap.Nr1,
                SubframeNullRepCap.Nr3,
                UserNullRepCap.Nr0,
                BwPartNullRepCap.Nr1,
                AllocationNullRepCap.Nr0,
                ColumnNullRepCap.Nr2,
                RowNullRepCap.Nr3);

            // Option 2: default values are set in the group interfaces, and then left to default in the method call:
            smbv.Source.Bb.Nr5G.Scheduling.Cell.RepCapCellNull = CellNullRepCap.Nr1;
            smbv.Source.Bb.Nr5G.Scheduling.Cell.Subf.RepCapSubframeNull = SubframeNullRepCap.Nr3;
            smbv.Source.Bb.Nr5G.Scheduling.Cell.Subf.User.RepCapUserNull = UserNullRepCap.Nr0;
            smbv.Source.Bb.Nr5G.Scheduling.Cell.Subf.User.BwPart.RepCapBwPartNull = BwPartNullRepCap.Nr1;
            smbv.Source.Bb.Nr5G.Scheduling.Cell.Subf.User.BwPart.Alloc.RepCapAllocationNull = AllocationNullRepCap.Nr0;
            smbv.Source.Bb.Nr5G.Scheduling.Cell.Subf.User.BwPart.Alloc.ApMap.Col.RepCapColumnNull = ColumnNullRepCap.Nr2;
            smbv.Source.Bb.Nr5G.Scheduling.Cell.Subf.User.BwPart.Alloc.ApMap.Col.Row.RepCapRowNull = RowNullRepCap.Nr3;
            // and then just use the Set() method without repeated capabilities:
            // Sending SOURce1:BB:NR5G:SCHed:CELL1:SUBF3:USER0:BWPart1:ALLoc0:APMap:COL2:ROW3:IMAGinary 10.0
            smbv.Source.Bb.Nr5G.Scheduling.Cell.Subf.User.BwPart.Alloc.ApMap.Col.Row.Imaginary.Set(10.0);

            // We can clone the 'Cell' interface and change the default cell from Nr1 to Nr2 without affecting the original 'Cell' interface:
            var cellNr2 = smbv.Source.Bb.Nr5G.Scheduling.Cell.Clone();
            cellNr2.RepCapCellNull = CellNullRepCap.Nr2;

            // Now we have an independent object cellNr2, and can send the same command for cell Nr2
            // All other repcap default values are unchanged:
            // SubframeNullRepCap.Nr3
            // UserNullRepCap.Nr0
            // BwPartNullRepCap.Nr1
            // AllocationNullRepCap.Nr0
            // ColumnNullRepCap.Nr2
            // RowNullRepCap.Nr3
            // Sending SOURce1:BB:NR5G:SCHed:CELL2:SUBF3:USER0:BWPart1:ALLoc0:APMap:COL2:ROW3:IMAGinary 10.0
            cellNr2.Subf.User.BwPart.Alloc.ApMap.Col.Row.Imaginary.Set(10.0);

            // Option 3: Combination of Options 1 and 2 - we use the default values from the group interfaces and explicitly define some of them:
            // Here we change the cell to 5 and Column to 4, all others are default from the group
            // Sending SOURce1:BB:NR5G:SCHed:CELL5:SUBF3:USER0:BWPart1:ALLoc0:APMap:COL4:ROW3:IMAGinary 10.0
            smbv.Source.Bb.Nr5G.Scheduling.Cell.Subf.User.BwPart.Alloc.ApMap.Col.Row.Imaginary.Set(
                10.0,
                CellNullRepCap.Nr5,
                SubframeNullRepCap.Default,
                UserNullRepCap.Default,
                BwPartNullRepCap.Default,
                AllocationNullRepCap.Default,
                ColumnNullRepCap.Nr4,
                RowNullRepCap.Default);

            // Closing the session
            smbv.Dispose();

            Console.Write("\n\nPress any key...");
            Console.ReadKey();
        }
    }
}
