Examples for the Rohde & Schwarz RsInstrument remote-control module

Preconditions:
- Installed R&S VISA 5.12+ ( https://www.rohde-schwarz.com/appnote/1dc02) or NI VISA 18.0+
- Your project uses .NET Framework 4.5+, .NET Standard 2.1+, .NET Core 3.1+

RsInstrument NuGet packages is not part of the examples. You have to restore it from https://www.nuget.org :
- In Visual Studio Professional go to the top menu Tools -> NuGet Packet Manager -> Manage NuGet Packages for Solution...
    It shows a yellow message that some packages are missing. Click on the 'Restore' button at the top right
	
- In other Visual Studio versions, use the Packet Manager Console command: Top menu View -> Other Windows -> Packet Manager Console
	PM> Update-Package -Id RsInstrument –reinstall