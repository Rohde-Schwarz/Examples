' Preconditions:
' - installed RsZnx IVI.NET instrument driver 3.30.0 or newer
' - installed R&S VISA 5.12.3+ or any other VISA '

Imports RohdeSchwarz.RsZnx
Imports Ivi.Driver

Module Module1

  Sub Main()

    ' ----------------------------------------------------------
    ' Initialization:
    '-----------------------------------------------------------
    ' Adjust the VISA Resource string to fit your instrument
    Dim resourceString1 = "TCPIP::10.205.0.172::INSTR" 'Standard LAN connection (also called VXI-11)
    Dim resourceString2 = "TCPIP::10.205.0.172::hislip0" 'Hi-Speed LAN connection - see 1MA208
    Dim resourceString3 = "GPIB::20::INSTR" 'GPIB Connection
    Dim driver = New RsZnx(resourceString1, True, False)

    ' switch device display on/off '
    driver.GeneralSettings.DisplayUpdateEnabled = True

    ' Add a New channel if it doesn't exist '
    Dim channel As Integer = 1
    Dim traceName = "Tr1"
    Dim window = 1
    Dim outPort = 1
    Dim inPort = 1

    driver.Channel.AddChannel(1, "")
    Dim channelRc = $"CH{channel.ToString()}"

    ' Create a New trace '
    driver.Channel.Channels(channelRc).Meas.SParameters.SelectSParameters(traceName, outPort, inPort)

    ' Select active trace '
    driver.Channel.Channels(channelRc).Trace.Select = traceName

    ' Change the format for trace '
    driver.Channel.Channels(channelRc).Format.TraceFormat = TraceFormat.Smith
    driver.Channel.Channels(channelRc).Format.GroupDelayAperturePoints = 10
          
    ' Display the trace in the display area '
    driver.Channel.Channels(channelRc).Trace.AssignTraceDiagramArea(traceName, 1)

    ' List the traces, assigned to a certain Channel '
    Dim channelsCatalog = driver.Channel.Channels(channelRc).Trace.ChannelCatalog
    Console.WriteLine("Channels\n" + channelsCatalog)

    Console.WriteLine("You should be able to see the added trace on the instrument now. Press OK to continue...")
    Console.ReadKey()

    ' Find the number for the trace '
    Dim traceDiagramNumber = driver.Channel.Channels(channelRc).Trace.DiagramNumber(traceName)

    ' Remove the trace from the diagram area '
    driver.Channel.Channels(channelRc).Trace.UnassignTraceDiagramArea(window, traceDiagramNumber.diagramNumber)

    ' Delete a trace with a specified trace name and channel. '
    driver.Channel.Channels(channelRc).Trace.Delete = traceName
                    
    driver.Dispose()

  End Sub

End Module
