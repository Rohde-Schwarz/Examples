clearvars;
clc;

% MATLAB Spectrum Analyzer SCPI example using visadev

%-------------------Write----------------------------------------
% Initialization:
%-----------------------------------------------------------
try
    % Adjust the VISA Resource string to fit your instrument
    specan = visadev("TCPIP::192.168.1.101::inst0");

    % Timeout for VISA Read Operations in milliseconds
    specan.Timeout = 3;
catch ME
    error ("Error initializing the instrument:\n%s", ME.message);
end

try
    % Identify instrument
    idnResponse = writeread(specan, "*IDN?");
    fprintf("\nInstrument Identification string: %s\n", idnResponse);

    % Reset the instrument
    writeline(specan, "*RST");

    % Clear the Error queue
    writeline(specan, "*CLS");

    % Switch OFF the continuous sweep
    writeline(specan, "INIT:CONT OFF");

    % Display update ON - switch OFF after debugging
    writeline(specan, "SYST:DISP:UPD ON");

    % Error Checking after Initialization block
    queryError(specan);

    %-----------------------------------------------------------
    % Basic Settings:
    %-----------------------------------------------------------
    % Setting the Reference Level
    writeline(specan, strcat("DISP:WIND:TRAC:Y:RLEV ",num2str(10.0)));

    % Setting the center frequency
    writeline(specan, strcat("FREQ:CENT ", num2str(3E9)));

    % Setting the span
    writeline(specan, strcat("FREQ:SPAN ", num2str(200E6)));

    % Setting the RBW
    writeline(specan, strcat("BAND ", num2str(100E3)));

    % Setting the VBW
    writeline(specan, strcat("BAND:VID ", num2str(300E3)));

    % Setting the sweep points
    writeline(specan, strcat("SWE:POIN ", num2str(10001)));

    % Error Checking after Basic Settings block
    queryError(specan);
    % -----------------------------------------------------------
    % SyncPoint 'SettingsApplied' - all the settings were applied
    % -----------------------------------------------------------
    % Sweep timeout - set it higher than the instrument measurement time
    specan.Timeout = 2;

    % Start the sweep
    writeline(specan, "INIT");
    fprintf("Waiting for the sweep to finish... ");
    tic
    % Using *OPC? query waits until the instrument finished the Acquisition
    writeread(specan, "*OPC?");
    toc

    % Error Checking after the acquisition is finished
    queryError(specan);

    % -----------------------------------------------------------
    % SyncPoint 'AcquisitionFinished' - the results are ready
    % -----------------------------------------------------------
    % Fetching the trace in ASCII format
    % -----------------------------------------------------------
    % Query the expected sweep points
    sweepPoints = str2double(writeread(specan, "SWE:POIN?"));
    fprintf("Fetching trace in ASCII format... ");
    tic
    writeline(specan, "FORM ASC");

    % sweepPoints is the maximum possible allowed count to read
    traceASC = str2num(writeread(specan, ":TRAC? TRACE1"));
    toc
    fprintf("Sweep points count: %d\n", size(traceASC, 2));

    % Error Checking after the data transfer
    queryError(specan);

    % -----------------------------------------------------------
    % Fetching the trace in Binary format
    % The transfer time of traces in binary format is shorter.
    % The traceBIN data and traceASC data are however the same.
    % -----------------------------------------------------------
    fprintf("Fetching trace in binary format... ");
    tic
    writeline(specan, "FORM REAL,32");
    writeline(specan, ":TRAC? TRACE1");
    traceBIN = readbinblock(specan,"single");
    read(specan,1);
    toc
    fprintf("Sweep points count: %d\n", size(traceBIN, 2));

    % Error Checking after the data transfer
    queryError(specan);

    % -----------------------------------------------------------
    % Setting the marker to max and querying the X and Y
    % -----------------------------------------------------------
    marker = 1;
    % Set the marker to the maximum point of the entire trace
    writeline(specan, sprintf("CALC1:MARK%d:MAX", marker));

    % Using *OPC? query waits until the marker is set
    writeread(specan, "*OPC?");
    markerX = writeread(specan, sprintf("CALC1:MARK%d:X?", marker));
    markerY = writeread(specan, sprintf("CALC1:MARK%d:Y?", marker));
    fprintf("Marker Frequency %0.1f Hz, Level %0.2f dBm\n", markerX, markerY);

    % Error Checking after the markers reading
    queryError(specan);
    
    % Displaying the trace
    plot(traceBIN); 
    % -----------------------------------------------------------
    % Making an instrument screenshot and transferring the file to the PC
    % -----------------------------------------------------------
    fprintf("Taking instrument screenshot and saving it to the PC... ");
    writeline(specan, "HCOP:DEV:LANG PNG;:MMEM:NAME 'c:\Temp\Device_Screenshot.png'"); % Hardcopy settings for taking a screenshot

    % Make the screenshot now
    writeline(specan, "HCOP:IMM");

    % Wait for the screenshot to be saved
    writeread(specan, "*OPC?");

    % Error Checking after the screenshot creation
    queryError(specan);
    writeline(specan, "MMEM:DATA? 'c:\Temp\Device_Screenshot.png'");
    imgBlock = readbinblock(specan);
    read(specan,1);
    fileID = fopen("c:\Temp\PC_Device_Screenshot.png", 'wb');
    fwrite(fileID, imgBlock, 'uint8');
    fclose(fileID);
    fprintf("OK\n");
    
    % Error Checking after the screenshot save
    queryError(specan);
    % -----------------------------------------------------------
    % Closing the session
    % -----------------------------------------------------------
    clear specan;
    % -----------------------------------------------------------
    % Error handling
    % -----------------------------------------------------------
catch ME
    switch ME.identifier
        case 'VISA_Instrument:ErrorChecking'
            % Perform your own additional steps here
            rethrow(ME);
        otherwise
            rethrow(ME)
    end
end

function queryError(specan)
%CHECKERROR Checks the instrument error stack for errors

errQueue = false;
errors = strings(0);
writeline(specan, "*STB?");
stb = readline(specan);
stb = str2double(stb);
errQueue = bitand(stb, 4) > 0;

% If there are errors, save it to the errors variable
if (errQueue == true)
    while 1
        response = writeread(specan, "SYST:ERR?");
        k = strfind(lower(response), "no error");
        if ~isempty (k)
            break
        end
        errors(end+1) = response;
    end
end

if ~isempty (errors)
    sizes = size(errors);
    errorsCount = sizes(2);
    allErrors = strjoin(errors, newline);
    if errorsCount == 1
        message = 'Instrument reports one error in the error queue';
    else
        message = sprintf('Instrument reports %d errors in the error queue', errorsCount);
    end
    throw(MException('VISA_Instrument:ErrorChecking', '%s:%s%s', message, newline, allErrors));
end
end

