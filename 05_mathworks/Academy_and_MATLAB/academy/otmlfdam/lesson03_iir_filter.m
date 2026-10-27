%% Filter Design and Analysis Methods: design an IIR filter
% Source: https://matlabacademy.mathworks.com/v1/portal.html?course=otmlfdam#chapter=2v1&lesson=3&section=4
% Both graded tasks received "Correct!" on 25 Sep 2026.
% INPUT: the course NoisyFlute.wav is required and is not bundled.
% TOOLBOX: Signal Processing Toolbox.
% The designfilt call is observed generated code from the interactive task.
% Separate figures preserve its displays; this standalone replay has not
% been independently executed or graded as a GUI task.

%% Course setup
[flute,fs]=audioread("NoisyFlute.wav");
flute=flute(1:3*fs);
t=((0:numel(flute)-1)/fs)';
yin=chirp(t,2200,t(end),2500)*0.0005;
marked=flute+yin;
figure('Name','Input watermarked flute spectrum');
pwelch(marked,[],[],[],fs);

%% Tasks 1-2: bandpass IIR with Hz specifications
% The task output was explicitly named designedFilter.
designedFilter=designfilt('bandpassiir', ...
    'StopbandFrequency1',2100, ...
    'PassbandFrequency1',2200, ...
    'PassbandFrequency2',2500, ...
    'StopbandFrequency2',2600, ...
    'StopbandAttenuation1',60, ...
    'PassbandRipple',1, ...
    'StopbandAttenuation2',60, ...
    'SampleRate',16000, ...
    'ScaleSOS',true);
figure('Name','Designed IIR bandpass response');
freqz(designedFilter,[],fs);

%% Course filtering and spectrum
yout=filter(designedFilter,marked);
figure('Name','IIR-filtered flute spectrum');
pwelch(yout,[],[],[],fs);

%% Verified ungraded playback example
% Academy reported a completed section with no outputs and Stop disabled.
% Commands ran; no hearing or subjective quality comparison is claimed.
soundsc(yin,fs);
pause(3.5);
soundsc(yout,fs);
