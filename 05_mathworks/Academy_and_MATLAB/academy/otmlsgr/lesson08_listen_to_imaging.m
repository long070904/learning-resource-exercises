%% Signal Generation and Resampling: verified imaging exercise
% Source: https://matlabacademy.mathworks.com/details/signal-generation-and-resampling/otmlsgr
% Lesson: Effect of Imaging > Listen to Imaging.
% Both tasks received "Correct!" in the hosted Academy runtime.
% The background slides and explanatory follow-up were reviewed only.
% No audio listening or quality assessment is claimed.
% Export adaptation: named figures preserve the separate Live Script plots.
% This .m figure arrangement has been statically reviewed, not executed.

%% Course-provided startup
fs=3000;
t=0:1/fs:0.5;
sig=sin(2*pi*1200*t);
figure('Name','Course startup - original spectrum');
pspectrum(sig,fs);

%% Task 1: insert samples at six times the original sample rate
sigbad=upsample(sig,6);
figure('Name','Task 1 - zero-insertion spectrum');
pspectrum(sigbad,fs*6);

%% Task 2: suppress the imaging components
sigfilt=lowpass(sigbad,fs/2,fs*6);
figure('Name','Task 2 - filtered upsampling spectrum');
pspectrum(sigfilt,fs*6);

% The further-practice explanation added no separate execution count.
