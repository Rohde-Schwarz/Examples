% GitHub examples repository path: VectorNetworkAnalyzers/MATLAB

% Created 2025/11

% Author:                     Miloslav Macko
% Version Number:             1
% Date of last change:        2025/11/27
% Requires:                   R&S ZNA / ZNB
%                             Installed VISA e.g. R&S VISA 7.x or newer

% Description:    Example for ZNx segmented sweep performed on one channel

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
    % io = RsInstrument('TCPIP::10.102.73.16::hislip0', 0, reset, 'SelectVisa=Socket'); % No VISA installation needed

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

    % RF Setup first
    io.write('SYSTEM:DISPLAY:UPDATE ON'); % Be sure to have the display updated whilst remote control
    io.write('INIT:CONT OFF'); % Set single sweep mode
    io.write('SENSe:SWEep:TIME:AUTO ON'); % Auto Sweep time
    io.write('TRIGger:SEQuence:SOURce IMMediate'); % Trigger immediate (Auto)
    io.write('AVERage OFF'); % Averaging disabled
    io.write('SEGment:CLEar'); % Deletes all sweep segments in the channel
    io.queryOpc();


    % Define Segment 1 for CH1
    % Ch1 Trc1 already exists by default
    io.write('CALCULATE1:PARAMETER:SDEFINE ''Trc1'', ''S22'''); % Reconfigure the trace Trc1 to S22
    io.write('DISPLAY:WINDOW1:TRACE:EFEED ''Trc1'''); % Feed it again to the window
    io.write('SENSe1:SEGMent1:ADD'); % Add Segment 1
    io.write('SENSe1:SEGMent1:FREQuency:STARt 500MHz'); % Start Frequency
    io.write('SENSe1:SEGMent1:FREQuency:STOP 900MHz'); % Stop Frequency
    io.write('SENSe1:SEGMent1:SWEep:POINts 401'); % No of Sweep Points
    io.write('SENSe1:SEGMent1:POWer:LEVel 10'); % Output Power Level
    io.write('SENSe1:SEGMent1:BWIDth 500Hz'); % RBW
    io.queryOpc();

    % Define Segment 2 for CH1
    % Using the complete command including "SENSe" will define the channel the changes will be applied to
    io.write('SENSe1:SEGMent2:ADD'); % Add Segment 2
    io.write('SENSe1:SEGMent2:FREQuency:STARt 1200MHz'); % Start Frequency
    io.write('SENSe1:SEGMent2:FREQuency:STOP 2400MHz'); % Stop Frequency
    io.write('SENSe1:SEGMent2:SWEep:POINts 501'); % No of Sweep Points
    io.write('SENSe1:SEGMent2:POWer:LEVel 0'); % Output Power Level
    io.write('SENSe1:SEGMent2:BWIDth 1000Hz'); % RBW
    io.queryOpc();

    % Initiate sweep and capture measurement data
    io.write('SWEep:TYPE SEGMent'); % Segmented sweep mode
    io.queryOpc();

    % Perform sweep and wait for it to finish
    fprintf('\nSweep Init...\n');
    io.writeWithOpc('INIT');
    fprintf('Finished Sweep\n');

    % Get Trace Data for CH1
    data = io.binary.queryBinOrAsciiFloatArray('FORM REAL,32;CALCulate1:DATA? SDATa');
    [sX, sY] = size(data);
    fprintf('\nCH1 Trace Result Data is an array of %d elements.\n\n', sX);

    % Add markers and get the results for CH1
    io.writeWithOpc('CALCulate1:MARKer1:STATe ON'); % Activate Marker 1
    io.writeWithOpc('CALCulate1:Marker1:FUNCtion:EXECute MINimum'); % Assign Minimum Function to Marker 1
    m1Min = io.query('CALCulate1:MARKer1:FUNCtion:RESult?'); % Read the result X,Y
    fprintf('\nResult for CH1 Marker 1 (maximum) is: %s\n\n', m1Min)

    io.writeWithOpc('CALCulate1:MARKer2:STATe ON'); % Activate Marker 2
    io.writeWithOpc('CALCulate1:Marker2:FUNCtion:EXECute MAXimum'); % Assign Maximum Function to Marker 2
    m2Max = io.query('CALCulate1:MARKer2:FUNCtion:RESult?'); % Read the result
    fprintf('\nResult for CH1 Marker 2 (minimum) is: %s\n\n', m2Max);

    io.writeWithOpc('CALCulate1:MARKer3:STATe ON'); % Activate Marker 3
    io.writeWithOpc('CALCulate1:Marker3:X 2 GHz'); % Set to a dedicated Frequency
    m3freq = io.queryDouble('CALCulate1:MARKer3:Y?'); % Read the Y result
    fprintf('\nResult for CH1 Marker 3 on 2 GHz is: %0.2f dB\n\n', m3freq);

    % -----------------------------------------------------------
    % Closing the session
    % -----------------------------------------------------------
    io.close(); % Closing the session to the instrument
    % -----------------------------------------------------------
catch ME
    if exist('io', 'var')
        io.close();
    end
    error(ME.message);
end
