' Hello World example for any R&S instrument

Imports System

' .NET component providing all the necessary VISA extended functionalities. Install as NuGet from www.nuget.org
Imports RohdeSchwarz.RsInstrument
' Preconditions:
' - R&S VISA 5.12.1+ (or NI VISA 18+)
' - Resource string adjusted to fit your instrument physical connection
'
' Before starting the program, change the appropriate resource string to fit your instrument interface
' and use it in the RsInstrument() constructor method

Module Program
  Sub Main(args As String())

    Dim instr
    Try ' Separate try-catch for initialization prevents accessing uninitialized object
      ' ----------------------------------------------------------
      ' Initialization:
      '-----------------------------------------------------------
      ' Adjust the VISA Resource string to fit your instrument
      Dim resourceString1 = "TCPIP::10.120.0.110::INSTR" 'Standard LAN connection (also called VXI-11)
      Dim resourceString2 = "TCPIP::10.120.0.110::hislip0" 'Hi-Speed LAN connection - see 1MA208
      Dim resourceString3 = "GPIB::20::INSTR" 'GPIB Connection
      Dim resourceString4 = "USB::0x0AAD::0x0119::022019943::INSTR" 'USB-TMC (Test and Measurement Class)
      Dim resourceString5 = "RSNRP::0x0095::104015::INSTR" 'R&S Powersensor NRP-Z86

      instr = New RsInstrument(resourceString1)
    Catch e As RsInstrumentException
      Console.WriteLine($"Error initializing the instrument session: {vbLf} {e.Message}" )
      
      Console.Write($"{vbLf}Press any key ...")
      Console.ReadKey()
      return
    End Try

    Dim idn = instr.Query("*IDN?")
    Console.WriteLine($"Hello, I am: '{idn}'")
    Console.WriteLine($"RsInstrument Driver Version: {instr.Identification.DriverVersion}, Core Version: {instr.Identification.CoreVersion}")
    Console.WriteLine($"Visa Manufacturer: '{instr.Identification.VisaManufacturer}'")
    Console.WriteLine($"Instrument Name: '{instr.Identification.InstrumentFullName}'")
    Dim options As List(Of String) = instr.Identification.InstrumentOptions
    Console.WriteLine($"Instrument installed options: '{String.Join(",", options.ToArray())}'")
    
    Console.Write($"{vbLf}Press any key ...")
    Console.ReadKey()

    instr.Dispose()

  End Sub
End Module