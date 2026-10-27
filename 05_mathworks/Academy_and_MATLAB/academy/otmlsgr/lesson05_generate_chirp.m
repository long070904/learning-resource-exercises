%% Signal Generation and Resampling: verified chirp exercise
% Source: https://matlabacademy.mathworks.com/details/signal-generation-and-resampling/otmlsgr
% Lesson: Generate a Chirp.
% Tasks 1-3 each received "Correct!" in the hosted Academy runtime.
% INPUT: NoisyFlute.wav is supplied by the course and is not bundled here.
% The ungraded follow-up completed with two outputs and counts as one example.
% No audio listening or subjective assessment is claimed.
% Export adaptation: named figures preserve the separate Live Script plots.
% This .m figure arrangement has been statically reviewed, not executed.

%% Course-provided startup
[flute,fs]=audioread("NoisyFlute.wav");
flute=flute(1:7*fs);
n=numel(flute);
t=(0:n-1)'/fs;
figure('Name','Course startup - flute spectrum');
pspectrum(flute,fs);

%% Task 1: create a frequency sweep from 6000 to 7000 Hz
wm=chirp(t,6000,t(end),7000);
figure('Name','Task 1 - chirp power spectrum');
pspectrum(wm,fs);

%% Task 2: inspect how the sweep changes over time
figure('Name','Task 2 - chirp spectrogram');
pspectrum(wm,fs,"spectrogram");

%% Task 3: combine the recording and chirp
marked=flute+wm;
figure('Name','Task 3 - marked flute power spectrum');
pspectrum(marked,fs);

%% Ungraded follow-up: inspect and reduce the chirp watermark
% The first plot uses the previous full-amplitude watermark. The second
% uses a chirp amplitude scaled to 0.002 of that value.
figure('Name','Ungraded follow-up - full-amplitude watermark spectrogram');
pspectrum(marked,fs,"spectrogram");
marked=flute+0.002*wm;
figure('Name','Ungraded follow-up - quieter watermark spectrogram');
pspectrum(marked,fs,"spectrogram");
