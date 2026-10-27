%% Filter Design and Analysis Methods: interactively design a filter
% Source: https://matlabacademy.mathworks.com/details/filter-design-and-analysis-methods/otmlfdam
% All three graded tasks received "Correct!" on 25 Sep 2026.
% INPUT: the course NoisyFlute.wav is required and is not bundled.
% TOOLBOX: Signal Processing Toolbox.
% Task 1 was performed with the Design Filter Live Editor task. The
% designfilt call below is its observed generated code, not a claim that
% this plain-script replay passed the interactive-task grader.
% Separate named figures preserve displays outside Live Editor; the
% standalone replay has not been independently executed.

%% Course signal setup
[flute,fs]=audioread("NoisyFlute.wav");
flute=flute(1:3*fs);
t=((0:numel(flute)-1)/fs)';
yin=chirp(t,2200,t(end),2500)*0.0005;
marked=flute+yin;
figure('Name','Watermarked flute spectrum');
pwelch(marked,[],[],[],fs);

%% Task 1: generated code from the bandpass FIR defaults
% No sample rate argument is supplied: the design frequencies below are
% normalized, as in the generated course code.
designedFilter=designfilt('bandpassfir', ...
    'StopbandFrequency1',0.35, ...
    'PassbandFrequency1',0.45, ...
    'PassbandFrequency2',0.55, ...
    'StopbandFrequency2',0.65, ...
    'StopbandAttenuation1',60, ...
    'PassbandRipple',1, ...
    'StopbandAttenuation2',60);
figure('Name','Generated bandpass FIR response');
freqz(designedFilter);

%% Task 2: apply the designed filter
yout=filter(designedFilter,marked);

%% Task 3: inspect the filtered spectrum
figure('Name','Filtered watermarked flute spectrum');
pwelch(yout,[],[],[],fs);

% The follow-up was conceptual. Its optional Run repeated graded code and
% does not count as an additional ungraded activity.
