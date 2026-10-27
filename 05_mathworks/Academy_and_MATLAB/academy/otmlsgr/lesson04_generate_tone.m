%% Signal Generation and Resampling: verified tone exercise
% Source: https://matlabacademy.mathworks.com/details/signal-generation-and-resampling/otmlsgr
% Lesson: Generate a Tone (2/2).
% Tasks 1-4 each received "Correct!" in the hosted Academy runtime.
% INPUT: NoisyFlute.wav is supplied by the course and is not bundled here.
% The separate ungraded follow-up completed with one output. Its soundsc
% command executed, but listening or subjective audio assessment is not claimed.
% Export adaptation: named figures preserve the separate Live Script plots.
% This .m figure arrangement has been statically reviewed, not executed.

%% Course-provided startup
[flute,fs]=audioread("NoisyFlute.wav");
flute=flute(1:7*fs);
figure('Name','Course startup - flute spectrum');
pspectrum(flute,fs);

%% Task 1: create one sample index for each audio value
t=(0:numel(flute)-1)';

%% Task 2: convert sample indices to seconds
t=t/fs;

%% Task 3: generate a six-kilohertz watermark tone
wm=sin(2*pi*6000*t);
figure('Name','Task 3 - watermark tone spectrum');
pspectrum(wm,fs);

%% Task 4: add the tone to the recording
marked=flute+wm;
figure('Name','Task 4 - marked flute spectrum');
pspectrum(marked,fs);

%% Ungraded follow-up: reduce the watermark amplitude
% This changes the watermark amplitude to one thousandth of its earlier value.
% Verified runtime status: section completed with one output.
marked=0.001*wm+flute;
figure('Name','Ungraded follow-up - quieter watermark spectrum');
pspectrum(marked,fs);
soundsc(marked,fs);
