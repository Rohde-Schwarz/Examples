% This example requires MATLAB Instrument Control Toolbox
% It uses .NET assembly called Ivi.Visa
% Preconditions:
% - Installed R&S VISA 5.11.0 or later with R&S VISA.NET
% - For resourceString5 (NRP-Zxx control, you need to install the R&S NRP-Toolkit)

% General example of an *IDN? query using VISA Raw connection

clear;
close all;
clc;

resourceString1 = 'TCPIP::192.168.1.101::inst0'; % Standard LAN connection (also called VXI-11)
resourceString2 = 'TCPIP::192.168.1.101::hislip0'; % Hi-Speed LAN connection - see 1MA208
resourceString3 = 'TCPIP::192.168.1.101::5025::SOCKET'; % Raw Socket connection on port 5025
resourceString4 = 'GPIB::20::INSTR'; % GPIB Connection
resourceString5 = 'USB::0x0AAD::0x0119::022019943::INSTR'; % USB-TMC (Test and Measurement Class)
resourceString6 = 'RSNRP::0x0095::104015::INSTR'; % R&S Powersensor NRP-Z86

% Opening VISA session to the instrument
io = visadev(resourceString3);
flush(io)
% Instrument Identification
idnResponse = writeread(io, "*IDN?");

fprintf('Hello, I am\t%s\n', idnResponse);