function data=NRPxxP_TraceData_ICT_V02
%{
Created 2023/07

Author:                     Winfried Jansen
Version Number:             2
Date of last change:        2023/07/19
Requires:                   R&S NRPxxP, FW 1.10 or newer
                            Installed VISA e.g. R&S Visa 7.2.x or newer
                            Matlab 2023a or newer incl. Instrument Control
                            Toolbox

Description: Setup of trace measurement and read out data


General Information:

Please always check this example script for unsuitable setting that may
destroy your DUT before connecting it to the instrument!
This example does not claim to be complete. All information has been
compiled with care. However, errors can not be ruled out.
%}


clear
close all
clc;

%open the connection
try
    NRPxxP = visadev('USB0::0x0AAD::0x0143::100111::INSTR');
    configureTerminator(NRPxxP,"LF");
catch ME
    error ('Error initializing the instrument:\n%s', ME.message);
end

%reset device 
writeline(NRPxxP,'*RST;*CLS');
writeread(NRPxxP, '*OPC?');
data1 = writeread(NRPxxP, '*IDN?');
disp(data1);

%setup the measurement
writeline(NRPxxP,'INIT:CONT OFF');
writeline(NRPxxP,'SENS:FUNC "XTIM:POW"');
writeline(NRPxxP,'SENS:FREQ 1.000000e+009');
 
% trace settings
writeline(NRPxxP,'SENS:TRAC:POIN 500');                
number_points=str2double(writeread(NRPxxP,'SENS:TRAC:POIN?'));
writeline(NRPxxP,'SENS:TRAC:TIME 10e-6');               
trace_length_s=str2double(writeread(NRPxxP,'SENS:TRAC:TIME?'));
writeline(NRPxxP,'SENS:TRAC:OFFS:TIME 0');               
writeread(NRPxxP, '*OPC?');
 
%trigger settings
writeline(NRPxxP,'TRIG:ATR:STAT OFF');               
writeline(NRPxxP,'TRIG:SOUR INT');                      
writeline(NRPxxP,'TRIG:LEV 10e-6');                    
writeline(NRPxxP,'TRIG:SLOP POS');
writeline(NRPxxP,'TRIG:COUN 1');
writeline(NRPxxP,'TRIG:DELay -10e-6');                  
writeline(NRPxxP,'TRIGger:HYSTeresis 0.5');
writeline(NRPxxP,'TRIGger:DTIME 0');
writeline(NRPxxP,'TRIG:Hold 0');
writeread(NRPxxP, '*OPC?');
                                              
%averaging settings
writeline(NRPxxP,'SENS:TRACE:AVER:COUN 8' );
writeline(NRPxxP,'SENS:TRACE:AVER:STAT ON' );
writeline(NRPxxP,'SENS:TRACE:AVER:TCON REP' );
writeline(NRPxxP,'SENS:AVER:RES' );
writeline(NRPxxP,'SENS:TRACE:REAL OFF' );
writeline(NRPxxP,'SENS:TRACE:MEAS:STAT OFF' );
writeread(NRPxxP, '*OPC?');
 

%Initiate a measurement
writeline(NRPxxP,'FORM REAL,32');
writeline(NRPxxP,'FORM:BORD NORM');
writeline(NRPxxP,'STAT:OPER:MEAS:NTR 2');
writeline(NRPxxP,'STAT:OPER:MEAS:PTR 0');
writeline(NRPxxP,'STAT:OPER:TRIG:NTR 2');
writeline(NRPxxP,'STAT:OPER:TRIG:PTR 0');
writeline(NRPxxP,'INIT:IMM');
% waiting for the end of the measurement
n=0;
while n < 2
    n=str2double(writeread(NRPxxP,'STAT:OPER:MEAS:EVEN?'));
    pause(10e-3);
end

%get the measurement result
writeline(NRPxxP,'FETC?');
data_trace=readbinblock(NRPxxP,"single");

%plot the result
x=linspace(0,trace_length_s,number_points);
p=plot(x,data_trace);
xlabel('time / us');
ylabel('power / W');
