%% Filter Design and Analysis Methods: compute frequency response
% Source: https://matlabacademy.mathworks.com/v1/portal.html?course=otmlfdam#chapter=4v1&lesson=3&section=1
% The graded task received "Correct!" on 25 Sep 2026 after selecting
% Display filter response > Group delay for designedFIR. The generated code
% displayed FIR frequency response and group delay. One ungraded code
% example extracted the response and plotted its magnitude; its section
% completed with one output in Academy.
% INPUT: the course NoisyFlute.wav is required and is not bundled.
% TOOLBOX: Signal Processing Toolbox.
% Separate named figures retain the displays; this standalone arrangement
% has not been independently executed.

%% Course signal setup
[flute,fs]=audioread("NoisyFlute.wav");
flute=flute(1:3*fs);
t=((0:numel(flute)-1)/fs)';
yin=chirp(t,2200,t(end),2500)*0.0005;
marked=flute+yin;

%% Course FIR design
designedFIR=designfilt('bandpassfir', ...
    'StopbandFrequency1',2100, ...
    'PassbandFrequency1',2200, ...
    'PassbandFrequency2',2500, ...
    'StopbandFrequency2',2600, ...
    'StopbandAttenuation1',80, ...
    'PassbandRipple',1, ...
    'StopbandAttenuation2',60, ...
    'SampleRate',16000);

%% Generated response and group-delay displays
figure('Name','FIR frequency response');
freqz(designedFIR,[],fs);
figure('Name','FIR group delay');
grpdelay(designedFIR,[],fs);
% Course feedback describes a constant group delay of 212 samples.

%% Verified ungraded magnitude-response example
[h,f]=freqz(designedFIR,[],fs);
figure('Name','Extracted FIR magnitude response');
plot(f,abs(h));
