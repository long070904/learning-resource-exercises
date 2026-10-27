%% Signal Generation and Resampling: verified aliasing exercise
% Source: https://matlabacademy.mathworks.com/details/signal-generation-and-resampling/otmlsgr
% Lesson: Effect of Aliasing > Listen to Aliasing.
% Both final submissions received "Correct!" in the hosted Academy runtime.
% Despite the lesson title, no audio listening or assessment is claimed.
% Export adaptation: named figures preserve the separate Live Script plots.
% This .m figure arrangement has been statically reviewed, not executed.

%% Course-provided startup
fs=24000;
t=0:1/fs:0.5;
sig=sin(2*pi*300*t)+sin(2*pi*3000*t);
figure('Name','Course startup - original spectrum and new Nyquist frequency');
pspectrum(sig,fs);
xline(2,"r--","New Nyquist Frequency");

%% Task 1: downsample directly
sigbad=downsample(sig,6);
figure('Name','Task 1 - direct downsampling spectrum');
pspectrum(sigbad,fs/6);

%% Task 2: filter before downsampling
% The accepted result variable must contain BOTH operations. An earlier
% attempt using sigbad instead was rejected; this corrected code passed.
sigfilt=lowpass(sig,fs/12,fs);
sigfilt=downsample(sigfilt,6);
figure('Name','Task 2 - filtered downsampling spectrum');
pspectrum(sigfilt,fs/6);

% The follow-up explanation was reviewed only. No further run is counted.
