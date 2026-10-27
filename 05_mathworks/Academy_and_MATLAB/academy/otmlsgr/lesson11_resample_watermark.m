%% Signal Generation and Resampling: verified watermark rate conversion
% Source: https://matlabacademy.mathworks.com/details/signal-generation-and-resampling/otmlsgr
% Lesson: Resample a Watermark. All four tasks received "Correct!" in Academy.
% INPUTS: NoisyFlute.wav and bird-call-in-spring.mp3 are real course assets.
% They are not bundled here and are required to run this file elsewhere.
% Saved-script adaptation: separate figures retain each spectrum when this
% plain .m file runs outside the Live Editor. This figure arrangement was not
% separately executed in the Academy checks; the computations are preserved.

%% Course-provided startup
[flute,fs]=audioread("NoisyFlute.wav");
flute=flute(1:7*fs);
fluteup=resample(flute,2,1);
fsup=fs*2;
figure('Name','Flute at the target sample rate');
pspectrum(fluteup,fsup);

%% Task 1: import the bird recording and its sample rate
[birds,fsb]=audioread("bird-call-in-spring.mp3");
figure('Name','Original bird recording spectrum');
pspectrum(birds,fsb);

%% Task 2: average across audio channels
birds=mean(birds,2);

%% Task 3: calculate the rational sample-rate conversion
[p,q]=rat(fsup/fsb);

%% Task 4: resample the watermark at the target rate
birdsdown=resample(birds,p,q);
figure('Name','Resampled bird recording spectrum');
pspectrum(birdsdown,fsup);

%% Ungraded follow-up: invoke playback at each recording's sample rate
% Academy reported completion with no outputs. The pause separates playback.
% Audio was not heard or assessed by the agent.
soundsc(birds,fsb);
pause(numel(birds)/fsb+0.2);
soundsc(birdsdown,fsup);
