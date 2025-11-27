% GitHub examples repository path: VectorNetworkAnalyzers/MATLAB

% Created 2025/11

% Author:                     Miloslav Macko
% Version Number:             1
% Date of last change:        2025/11/27
% Requires:                   R&S ZNA / ZNB
%                             Installed VISA e.g. R&S VISA 7.x or newer

% Description:

% Creates four diagrams in one channel, with different S-parameters.
% Each diagram has two traces (magnitude and phase).
% Then, performs a single sweep and stores the touchstone s2p file into the instrument.
% The last step is copying that file to the control PC.

% General Information:

% Please always check this example script for unsuitable setting that may
% damage your equipment before connecting it to the instrument!

% This statement's precondition is:
% Needs the path to the RsInstrument.jar in the
% C:\Users\JohnSmith\AppData\Roaming\MathWorks\MATLAB\R2025b\javaclasspath.txt (example of the path)
import com.rohdeschwarz.rsinstrument.*

%-----------------------------------------------------------
% RsInstrument Driver version check:
%-----------------------------------------------------------
driverVersion = RsInstrument.getVersion();
fprintf('\nRsInstrument driver version: %s\n', driverVersion);

%-----------------------------------------------------------
% Initialization:
%-----------------------------------------------------------
try
    % Logger initialization - we will always log to the console.
    logger = ScpiLogger.asConsoleLogger();
    logger.setStartTimeOffsetOnFirstEntry(); % The first entry will have start timestamp of '00:00:00.000'
        
    logger.addTargetFile("myLogFile.txt"); % We can also add logging to a file
    logger.setState(true);
    logger.setLogStatusCheckOk(false); % If false, error check OK lines will not be logged
    logger.logRawInfo('My custom logging entry');
    logger.logRawInfoWithTimestamp('My custom logging entry with timestamp');
    reset = true;

    io = RsInstrument('TCPIP::10.102.73.16::hislip0', 0, reset, 'SelectVisa=Rs', logger); % SelectVisa=Rs
    % io = RsInstrument('TCPIP::10.102.73.16::hislip0', 0, reset, 'SelectVisa=Socket', logger); % No VISA installation needed

catch ME
    error ('Error initializing the instrument:\n%s', ME.message);
end

try
    idnResponse = io.identification.getIdnString();
    fprintf('\nInstrument Identification string: %s\n', idnResponse);

    % Communication session settings
    io.setVisaTimeoutMs(5000);                                  % Timeout for VISA Read Operations
    io.setOpcTimeoutMs(5000);                                   % Timeout for opc-synchronised operations
    io.setInstrumentStatusChecking(true);                       % Error check after each command, can be true or false

    % RF Settings first
    io.write('SYSTEM:DISPLAY:UPDATE ON'); % Be sure to have the display updated whilst remote control
    io.write('SENSe1:FREQuency:Start 700e6'); % Set start frequency to 700 MHz
    io.write('SENSe1:FREQuency:Stop 1.3e9'); % Set stop frequency to 1.3 GHz
    io.write('SENSe1:SWEep:POINts 501'); % Set number of sweep points
    io.queryOpc();

    % Prepare S11 measurement in Diagram 1
    io.write('CALCulate1:PARameter:MEAsure "Trc1", "S11"'); % Change active trace to S11 measurement
    io.write('CALCulate1:Format MAGNitude'); % Be sure to have active trace's format to dB Mag
    io.write('CALCulate1:PARameter:SDEFine "Trc2", "S11"'); % Add a second trace
    io.write('CALCulate1:Format PHASe'); % Change active trace's format to phase
    io.write('DISPlay:WINDow1:TRACe2:FEED "Trc2"'); % Display the second trace
    io.queryOpc();

    % Prepare S22 measurement in Diagram 2 like for S11 if not separately commented
    io.write('DISPlay:WINDow2:STATe ON'); % Add another diagram
    io.write('CALCulate1:PARameter:SDEFine "Trc3", "S22"'); % Add a third trace
    io.write('CALCulate1:Format MAGNitude');
    io.write('DISPlay:WINDow2:TRACe3:FEED "Trc3"');
    io.write('CALCulate1:PARameter:SDEFine "Trc4", "S22"');
    io.write('CALCulate1:Format PHASe');
    io.write('DISPlay:WINDow2:TRACe4:FEED "Trc4"');
    io.queryOpc();

    % Prepare S21 measurement in Diagram 3 like before if not separately commented
    io.write('DISPlay:WINDow3:STATe ON');
    io.write('CALCulate1:PARameter:SDEFine "Trc5", "S21"');
    io.write('CALCulate1:Format MAGNitude');
    io.write('DISPlay:WINDow3:TRACe3:FEED "Trc5"');
    io.write('CALCulate1:PARameter:SDEFine "Trc6", "S21"');
    io.write('CALCulate1:Format PHASe');
    io.write('DISPlay:WINDow3:TRACe4:FEED "Trc6"');
    io.queryOpc();

    % Prepare S12 measurement in Diagram 4 like before if not separately commented
    io.write('DISPlay:WINDow4:STATe ON');
    io.write('CALCulate1:PARameter:SDEFine "Trc7", "S12"');
    io.write('CALCulate1:Format MAGNitude');
    io.write('DISPlay:WINDow4:TRACe3:FEED "Trc7"');
    io.write('CALCulate1:PARameter:SDEFine "Trc8", "S12"');
    io.write('CALCulate1:Format PHASe');
    io.write('DISPlay:WINDow4:TRACe4:FEED "Trc8"');
    io.queryOpc();

    % Perform single sweep and wait for it to finish
    io.write('INIT1:CONTinuous OFF');
    fprintf('\nSweep Init...\n');
    io.writeWithOpc('INIT1:IMMediate');
    fprintf('Finished Sweep\n\n');

    % Save the measurement to a s2p file
    io.writeWithOpc('MMEMory:STORe:TRACe:PORTs 1, ''tracefile.s2p'', COMPlex, CIMPedance, 1, 2');
    % An S2P file does only contain real and imaginary part of each scatter parameter of the measurement.
    % To extract e.g. the magnitude and phase data of each trace, better use the command
    % MMEMory:STORe:TRACe:CHANnel 1, 'tracefile.s2p', FORM, LINPhase
    % Using just a file name, the file is stored in the default path:
    % C:\Users\Public\Documents\Rohde-Schwarz\ZNx

    % Reads the file from the instrument to the PC
    io.file.fromInstrumentToPc('tracefile.s2p', 'c:\temp\vna_pc_tracefile.s2p');

    % -----------------------------------------------------------
    % Closing the session
    % -----------------------------------------------------------
    io.close(); % Closing the session to the instrument
    % -----------------------------------------------------------

    fprintf('\nFinished. Touchstone file copied to the control PC, path c:\\temp\\vna_pc_tracefile.s2p\n\n');


catch ME
    if exist('io', 'var')
        io.close();
    end
    error(ME.message);
end
