%% Filter Design and Analysis Methods: design an FIR filter
% Source: https://matlabacademy.mathworks.com/v1/portal.html?course=otmlfdam#chapter=2v1&lesson=3&section=2
% All three GUI tasks received "Correct!" on 25 Sep 2026.
% INPUT: the course NoisyFlute.wav is required and is not bundled.
% TOOLBOX: Signal Processing Toolbox.
% The designfilt call is the observed generated code from the Design Filter
% task at the final accepted 80 dB lower-stopband setting. It is a replay,
% not an independently graded substitute for that interactive task.
% Separate named figures retain displays; the .m arrangement was not
% independently executed. The course asset sample rate was 16000 Hz.

%% Course setup
[flute,fs]=audioread("NoisyFlute.wav");
flute=flute(1:3*fs);
t=((0:numel(flute)-1)/fs)';
yin=chirp(t,2200,t(end),2500)*0.0005;
marked=flute+yin;
figure('Name','Input watermarked flute spectrum');
pwelch(marked,[],[],[],fs);

%% Tasks 1-3: Hz units, specified edges, and 80 dB first stopband
designedFilter=designfilt('bandpassfir', ...
    'StopbandFrequency1',2100, ...
    'PassbandFrequency1',2200, ...
    'PassbandFrequency2',2500, ...
    'StopbandFrequency2',2600, ...
    'StopbandAttenuation1',80, ...
    'PassbandRipple',1, ...
    'StopbandAttenuation2',60, ...
    'SampleRate',16000);
figure('Name','Designed FIR bandpass response');
freqz(designedFilter,[],fs);
info(designedFilter);

%% Course downstream filtering and display
yout=filter(designedFilter,marked);
figure('Name','FIR-filtered flute spectrum');
pwelch(yout,[],[],[],fs);

%% Verified ungraded playback example
% The section completed with no outputs in Academy. Playback commands ran;
% no claim is made that the agent heard or compared the audio.
soundsc(yin,fs);
pause(3.5);
soundsc(yout,fs);

% Separate verified GUI practice inspected Filter Information:
% lower-stopband attenuation 80 dB -> length 425 (order 424);
% lower-stopband attenuation 60 dB -> length 317 (order 316);
% restored 80 dB -> length 425. The increase is 108 coefficients.
% The GUI comparison is recorded in lesson02_fir_filter_gui.md and counts
% as one activity, not another executed standalone design.
