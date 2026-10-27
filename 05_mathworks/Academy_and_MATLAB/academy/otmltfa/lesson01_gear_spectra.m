%% Time-Frequency Analysis: time-varying gear box signal
% Source: https://matlabacademy.mathworks.com/details/time-frequency-analysis/otmltfa
% Both graded tasks received "Correct!" in Academy on 25 Sep 2026.
% INPUT: the course monitoredgearbox.mat is required and is not bundled.
% Observed workspace: healthyGear 1x15000, monitoredGear 1x40000, fs scalar.
% The sampling rate is loaded from the asset, not assumed from background text.
% Separate figures retain both plots outside the Live Editor; this display
% adaptation has not been independently executed in native MATLAB.

%% Course setup
load monitoredgearbox.mat;
whos;

%% Task 1: healthy gearbox power spectrum
figure('Name','Healthy gearbox power spectrum');
pspectrum(healthyGear,fs);

%% Task 2: monitored gearbox power spectrum
figure('Name','Monitored gearbox power spectrum');
pspectrum(monitoredGear,fs);

% Further practice consisted of conceptual notes only.
