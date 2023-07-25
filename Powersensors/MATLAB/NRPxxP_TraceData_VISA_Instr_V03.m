function data=NRPxxP_TraceData_VISA_Instr_V03
%{
Created 2023/07

Author:                     Winfried Jansen
Version Number:             3
Date of last change:        2023/07/20
Requires:                   R&S NRPxxP, FW 1.10 or newer
                            Installed VISA e.g. R&S Visa 7.2.x or newer
                            Matlab 2023a or newer incl. VISA_Instrument.m
                            V1.12 or newer

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
% add the path to the VISA_Instruments.m
addpath("C:\CAE\Mathworks\Matlab\R2023a");

%open the connection
try
    NRPxxP = VISA_Instrument('USB0::0x0AAD::0x0143::100111::INSTR'); % Adjust the VISA Resource string to fit your NRPxxP powersensor
    NRPxxP.SetTimeoutMilliseconds(7000); % Timeout for VISA Read Operations
catch ME
    error ('Error initializing the instrument:\n%s', ME.message);
end

%reset device 
NRPxxP.Write('*RST;*CLS');
NRPxxP.QueryString( '*OPC?');
data1 = NRPxxP.QueryString( '*IDN?');
disp(data1);

%setup the measurement
NRPxxP.Write('INIT:CONT OFF');
NRPxxP.Write('SENS:FUNC "XTIM:POW"');
NRPxxP.Write('SENS:FREQ 1.000000e+009');
 
% trace settings
NRPxxP.Write('SENS:TRAC:POIN 500');                
number_points=str2double(NRPxxP.QueryString('SENS:TRAC:POIN?'));
NRPxxP.Write('SENS:TRAC:TIME 10e-6');               
trace_length_s=str2double(NRPxxP.QueryString('SENS:TRAC:TIME?'));
NRPxxP.Write('SENS:TRAC:OFFS:TIME 0');               
NRPxxP.QueryString('*OPC?');
 
%trigger settings
NRPxxP.Write('TRIG:ATR:STAT OFF');               
NRPxxP.Write('TRIG:SOUR INT');                      
NRPxxP.Write('TRIG:LEV 10e-6');                    
NRPxxP.Write('TRIG:SLOP POS');
NRPxxP.Write('TRIG:COUN 1');
NRPxxP.Write('TRIG:DELay -10e-6');                  
NRPxxP.Write('TRIGger:HYSTeresis 0.5');
NRPxxP.Write('TRIGger:DTIME 0');
NRPxxP.Write('TRIG:Hold 0');
NRPxxP.QueryString( '*OPC?');
                                              
%averaging settings
NRPxxP.Write('SENS:TRACE:AVER:COUN 8' );
NRPxxP.Write('SENS:TRACE:AVER:STAT ON' );
NRPxxP.Write('SENS:TRACE:AVER:TCON REP' );
NRPxxP.Write('SENS:AVER:RES' );
NRPxxP.Write('SENS:TRACE:REAL OFF' );
NRPxxP.Write('SENS:TRACE:MEAS:STAT OFF' );
NRPxxP.QueryString( '*OPC?');
 

%Initiate a measurement
NRPxxP.Write('FORM REAL,32');
NRPxxP.Write('FORM:BORD NORM');
NRPxxP.Write('STAT:OPER:MEAS:NTR 2');
NRPxxP.Write('STAT:OPER:MEAS:PTR 0');
NRPxxP.Write('STAT:OPER:TRIG:NTR 2');
NRPxxP.Write('STAT:OPER:TRIG:PTR 0');
NRPxxP.Write('INIT:IMM');
% waiting for the end of the measurement
n=0;
while n < 2
    n=str2double(NRPxxP.QueryString('STAT:OPER:MEAS:EVEN?'));
    pause(10e-3);
end

%get the measurement result
data_trace=NRPxxP.QueryBinaryFloatData('FETC?');

%close the VISA connection
NRPxxP.Close();

%plot the result
x=linspace(0,trace_length_s,number_points);
p=plot(x,data_trace);
xlabel('time / us');
ylabel('power / W');