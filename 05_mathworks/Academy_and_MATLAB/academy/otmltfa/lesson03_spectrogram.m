%% Time-Frequency Analysis: spectrogram function
% Source: https://matlabacademy.mathworks.com/details/time-frequency-analysis/otmltfa
% All three graded tasks received "Correct!" on 25 Sep 2026.
% INPUT: the course monitoredgearbox.mat is required and is not bundled.
% Separate named figures preserve all three displays outside Live Editor;
% this standalone display arrangement was not independently executed.

%% Course setup
load monitoredgearbox.mat;
n=length(monitoredGear); % Observed course value: 40000.

%% Task 1: one rectangular window spanning the signal
figure('Name','Full-length rectangular-window spectrogram');
spectrogram(monitoredGear,ones(n,1),0,[],fs);

%% Task 2: default window, overlap, and transform length
figure('Name','Spectrogram with default parameters');
spectrogram(monitoredGear,[],[],[],fs);

%% Task 3: display frequency on the vertical axis
figure('Name','Spectrogram with frequency on the vertical axis');
spectrogram(monitoredGear,[],[],[],fs,"yaxis");

% Further practice reviewed the defaults conceptually, with no extra run.
