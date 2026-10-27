%% Supplied Further Practice example: filtertozero.mlx
% From FIR Filter Transient; no external data needed.
% Requires Signal Processing Toolbox.
% An outdated Design Filter live task could not restore its state. Its
% displayed generated code was retained using Convert to Code in Academy.
% Academy run verified 28 Sep 2026: three plots appeared, Stop disabled.
% Separate figures below are an independently untested display adaptation.

%% Generate a 3 Hz tone
fs = 25;
t = 0:1/fs:8;
sig = sin(2*pi*3*t);

%% Create a highpass filter at 10 Hz
designedFilter = designfilt('highpassfir', ...
    'FilterOrder',50,'CutoffFrequency',10, ...
    'SampleRate',fs);
figure; freqz(designedFilter.Coefficients,1,[],fs)

%% Filter the signal and mark the transient boundary
sigfilt = filter(designedFilter,sig);
figure; plot(t,sigfilt)
xline(t(50))

%% Remove the transient and plot the result
figure; plot(t(50:end),sigfilt(50:end))
