% This example requires MATLAB Instrument Control Toolbox
% Preconditions:
% - Installed R&S VISA 5.11.0 or later with R&S VISA.NET
%
%
% The example configures the spectrum analyzer to capture IQ data. 
% The IQ data is transferred to the PC and displayed.
%
% Inputs:  IP         - Spectrum Analyzer IP address as string
%          Freq       - Center Frequency in Hz
%          RefLev     - Reference Level in dBm
%          SampleRate - Sample Rate for IQ capture in Hz
%          NofSamples - Number of Samples to capture
%
% Outputs: IQ - captured IQ data
%
% Example:
%IP         = '10.0.0.177';
%Freq       = 1e9;
%RefLev     = 0;
%SampleRate = 20e6;
%NofSamples = 20e3;

clear all;
close all;
clc;

IP         = '192.168.1.101';
Freq       = 0.999e9;
RefLev     = 0.0;
SampleRate = 10e6;
NofSamples = 20e3;

clc;
%-----------------------------------------------------------
% Initialization:
%-----------------------------------------------------------
try
    % Adjust the VISA Resource string to fit your instrument
    specan = visadev(sprintf("TCPIP::%s::inst0",IP));
    % Timeout for VISA Read Operations in milliseconds; 
    specan.Timeout = 3000; 
catch ME
    error ('Error initializing the instrument:\n%s', ME.message);
end

try
    % Flush input and output buffers
    flush(specan);
    % Read identification string
    idnResponse = writeread(specan, "*IDN?");
    fprintf('\nInstrument Identification string: %s\n', idnResponse);
    % Reset the instrument
    writeline(specan, "*RST");
    % Clear the Error queue
    writeline(specan, "*CLS");

    if contains(idnResponse,"FSW-85")
        writeline(specan,"INP:TYPE INPUT2;*WAI");
    end %if

    % Switch OFF the continuous sweep
    writeline(specan, "INIT:CONT OFF");
    % Display update ON - switch OFF after debugging
    writeline(specan, "SYST:DISP:UPD ON"); 
    queryError(specan); % Error Checking after Initialization block
    
    %-----------------------------------------------------------
    % Open IQ Analyzer and set parameters
    %-----------------------------------------------------------
    % Setting the Reference Level
    writeline(specan, sprintf("DISP:WIND:TRAC:Y:RLEV %2.2f", RefLev));
    % Setting the center frequency and span
    writeline(specan, sprintf("FREQ:CENT %9.1f", Freq));
    writeline(specan,sprintf("FREQ:SPAN %8.1f", SampleRate));
    writeline(specan,"INIT:CONT ON");
    % Perform autolevelling in spectrum analyzer window 
    writeline(specan,"SENS:ADJ:LEV;*WAI");   
    % Open IQ Analyzer - Universal command for FSV / FSVA / FSW
    writeline(specan, "INST:CRE IQ, 'IQ Analyzer';*WAI");

    if contains(idnResponse,"FSW-85")
       writeline(specan,"INP:TYPE INPUT2;*WAI");
    end %if

    % Check for operation complete (OPC).
    writeread(specan, "*OPC?"); 
    % Error Checking
    queryError(specan);
    % Set IQ acquisition - sample rate
    writeline(specan, sprintf("TRAC:IQ:SRAT %d", SampleRate));
    % Set IQ acquisition - result length
    writeline(specan, sprintf("TRAC:IQ:RLEN %d", NofSamples)); 
    writeline(specan, "TRAC:IQ:DATA:FORM IQPair");
    writeline(specan, "INIT:CONT OFF");
    % This command tells the instrument to finish processing all the previous commands
    writeread(specan, "*OPC?"); 
    % Error Checking
    queryError(specan); 
    
    % -----------------------------------------------------------
    % IQ Measurement
    % -----------------------------------------------------------
    
    writeline(specan, "INIT:IMM");
    % Start the capture
    junk = writeread(specan, "*OPC?");
    % Error Checking after the acquisition is finished
    queryError(specan); 
    
    % -----------------------------------------------------------
    % Fetching the IQ data
    % -----------------------------------------------------------
    fprintf('Fetching IQ data... ');
    writeline(specan, "FORM REAL,32");
    % Transfer binary IQ data    
    writeline(specan,"TRACe:IQ:DATA:MEM?");
    DataVector = binblockread(specan,"float");
    % Read the remaining char from the end of the binblock transfer.
    junkChar = readline(specan);
    % Restore sweeping
    writeline(specan,"INIT:CONT ON"); 
    fprintf('done.\n');
    % Error Checking after the data transfer
    queryError(specan); 
        
    % -----------------------------------------------------------
    % Closing the session
    % -----------------------------------------------------------
    % Go to Local
    writeline(specan, "@LOC");
    % Error Checking
    queryError(specan);
    % Clear the session to the instrument
    clear specan 
    
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

%% Display IQ data

% Convert return data to complex number
IQData = DataVector(1:2:end) + 1j*DataVector(2:2:end);

% Time vector
x = (0 : (NofSamples-1)) ./ SampleRate;

% Plot time domain data
figure('name','Time-Domain IQ Signal');
subplot(311), plot(x, real(IQData)) %plot I data
title('real'), xlabel('time [sec]'), ylabel('Volt')
subplot(312), plot(x, imag(IQData)) %plot Q data
title('imaginary'), xlabel('time [sec]'), ylabel('Volt')
% Plot magnitude
subplot(313), plot(x, 20*log10(abs(IQData)) - 10*log10(50) + 30) 
title('magnitude'), xlabel('time [sec]'), ylabel('dBm')
movegui('northeast');

% Plot constellation diagram
figure('name','Constellation Diagram')
plot(real(IQData),imag(IQData),'.')
xlabel('I'), ylabel('Q')
axis square
movegui('southeast');

% Compute Time-Domain Power
V_RMS = sqrt( mean( abs(IQData).^2) );
P_dBm = 20 * log10( V_RMS ) - 10*log10(50) + 30;

fprintf('\nTime-Domain Power = %g dBm\n', P_dBm)

% Compute Power Spectrum
L = length(IQData);

NFFT = 2^nextpow2(L);

IQ = fft(IQData,NFFT);
IQ = flipud(fftshift(IQ)); 

% Move the Nyquist point to the right-hand side (pos freq) to be
% consistent with plot when looking at the positive half only.
IQ = [IQ(2:end,:); IQ(1,:)];
    
df = SampleRate/NFFT;
f = (1:NFFT).*df - SampleRate/2;

Pxx = IQ.*conj(IQ);

% Convert to dBm (50 Ohm load assumed)
Pxx = 10*log10(Pxx./50 *1000);

% IQ data are baseband data, set 0Hz == center frequency
f = f + Freq;

% Plot power spectrum
figure('name','Power Spectrum')
plot(f,Pxx), grid
xlabel('frequency [Hz]'), ylabel('Power [dBm]')
movegui('northwest');


function queryError(specan)
% QUERYERROR Checks the instrument error stack for errors

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
