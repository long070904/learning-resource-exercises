%% Time-Frequency Analysis: project - identify fan faults
% Source: https://matlabacademy.mathworks.com/v1/portal.html?course=otmltfa#chapter=5v1&lesson=1&section=1
% All seven graded tasks received "Correct!" on 25 Sep 2026.
% INPUT: the course monitoredfan.mat is required and is not bundled.
% TOOLBOXES: Signal Processing Toolbox (spectrogram, kaiser) and Wavelet
% Toolbox (cwt).
% Observed workspace: fs=2400, monitoredfan 30001x1, n=30001,
% fr=66.6667, frO=143.1300, frR=211.9600 (displayed precision).
% Values are loaded from the asset rather than reconstructed here.
% Separate named figures and a Task 4 semicolon preserve displays without
% dumping large matrices. These replay adaptations were not independently
% executed. Task 3 deliberately modifies the Task 2 axes.

%% Course setup
load monitoredfan.mat;

%% Task 1: default spectrogram
figure('Name','Default monitored fan spectrogram');
spectrogram(monitoredfan,[],[],[],fs);

%% Task 2: Kaiser window with 2048 samples and beta 19
w=kaiser(2048,19);
figure('Name','Windowed fan spectrogram with selected time range');
spectrogram(monitoredfan,w,[],[],fs);

%% Task 3: inspect the 3-5 second range on the preceding axes
ylim([3 5]);

%% Task 4: retain the spectral matrix
% The Academy submission omitted this semicolon.
[s,f,t,ps]=spectrogram(monitoredfan,w,[],[],fs);

%% Task 5: first time slice
firstslice=ps(:,1);
figure('Name','First monitored fan spectrum slice');
plot(f,firstslice);

%% Task 6: last time slice
lastslice=ps(:,end);
figure('Name','Last monitored fan spectrum slice');
plot(f,lastslice);

%% Task 7: bump-wavelet scalogram
figure('Name','Monitored fan scalogram with bump wavelet');
cwt(monitoredfan,"bump",fs);

% Conceptual course feedback identifies a strongest component near 573 Hz
% as an outer-race harmonic, indicating a broken outer race. The feedback
% quotes about 143.14 Hz; the workspace displayed frO=143.1300. These are
% course-provided explanations/values, not newly measured diagnoses.
