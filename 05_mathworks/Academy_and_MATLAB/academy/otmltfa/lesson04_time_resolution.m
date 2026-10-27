%% Time-Frequency Analysis: time resolution
% Source: https://matlabacademy.mathworks.com/details/time-frequency-analysis/otmltfa
% Both graded tasks received "Correct!" on 25 Sep 2026.
% INPUT: the course monitoredgearbox.mat is required and is not bundled.
% Separate figures retain the default and adjusted displays; this standalone
% display adaptation was not independently executed.

%% Course starting display
load monitoredgearbox.mat;
figure('Name','Default gearbox spectrogram');
spectrogram(monitoredGear,[],[],[],fs);

%% Task 1: define the 2500-sample Hamming window
w=hamming(2500);

%% Task 2: use the shorter window
figure('Name','Gearbox spectrogram with a 2500-sample window');
spectrogram(monitoredGear,w,[],[],fs);

% Conceptual course feedback states that additional frequencies appear at
% 3 seconds. This is provided feedback, not a new numerical measurement.
