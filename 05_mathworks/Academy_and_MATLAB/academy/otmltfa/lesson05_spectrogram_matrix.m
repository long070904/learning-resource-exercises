%% Time-Frequency Analysis: spectrogram matrix
% Source: https://matlabacademy.mathworks.com/v1/portal.html?course=otmltfa#chapter=3v1&lesson=2&section=3
% All three graded tasks received "Correct!" on 25 Sep 2026.
% INPUT: the course monitoredgearbox.mat is required and is not bundled.
% Observed dimensions: s 2049x31 complex; f 2049x1; t 1x31; ps 2049x31.
% The sampling rate comes from the asset and is not hardcoded.
% Separate named figures preserve the first and last slices outside Live
% Editor; the standalone display adaptation was not independently executed.

%% Course setup
load monitoredgearbox.mat;

%% Task 1: retain spectral values and their axes
% Academy submission omitted the semicolon and displayed these outputs.
% A semicolon avoids dumping large matrices in this standalone script.
[s,f,t,ps]=spectrogram(monitoredGear,hamming(2500),[],[],fs);

%% Task 2: first time slice
firstslice=ps(:,1);
figure('Name','First gearbox spectrogram time slice');
plot(f,firstslice);

%% Task 3: last time slice
lastslice=ps(:,end);
figure('Name','Last gearbox spectrogram time slice');
plot(f,lastslice);

% Further practice was conceptual only. Course feedback describes an
% initially healthy signal followed by an added 2 kHz fault component.
