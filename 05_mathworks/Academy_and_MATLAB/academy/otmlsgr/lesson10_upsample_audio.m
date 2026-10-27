%% Signal Generation and Resampling: verified audio upsampling exercise
% Source: https://matlabacademy.mathworks.com/details/signal-generation-and-resampling/otmlsgr
% Lesson: Upsample Audio. All five tasks received "Correct!" in Academy.
% INPUT: the course NoisyFlute.wav is required and is not bundled here.
% Tasks 1-2 below record the original accepted stage; Task 3 then replaces
% the zero-insertion operation, as required by the later task.
% Export adaptation: named figures preserve the separate Live Script plots.
% This .m figure arrangement has been statically reviewed, not executed.

%% Course-provided startup
[flute,fs]=audioread("NoisyFlute.wav");
flute=flute(1:7*fs);
n=numel(flute);
t=(0:n-1)';
t=t/fs;
figure('Name','Course startup - flute spectrum');
pspectrum(flute,fs);

%% Task 1: historical zero-insertion stage
fluteup=upsample(flute,2);

%% Task 2: assign the doubled sample rate
fsup=2*fs;
figure('Name','Task 2 - zero-insertion spectrum');
pspectrum(fluteup,fsup);

%% Task 3: accepted replacement using resample
% In Academy this replaced the Task 1 line before rerunning the spectrum.
% Here it is a separate stage that overwrites fluteup with the final result.
fluteup=resample(flute,2,1);
figure('Name','Task 3 - resampled flute spectrum');
pspectrum(fluteup,fsup);

%% Task 4: generate a chirp on the new time grid
tup=(0:numel(fluteup)-1)'/fsup;
wm=chirp(tup,12000,tup(end),14000);

%% Task 5: add a low-amplitude watermark
marked=fluteup+0.0001*wm;
figure('Name','Task 5 - marked upsampled flute spectrum');
pspectrum(marked,fsup);

%% Ungraded follow-up: invoke playback for both signals
% Academy reported completion with no outputs. The pause separates playback.
% Audio was not heard or assessed by the agent.
soundsc(fluteup,fsup);
pause(numel(fluteup)/fsup+0.2);
soundsc(marked,fsup);

