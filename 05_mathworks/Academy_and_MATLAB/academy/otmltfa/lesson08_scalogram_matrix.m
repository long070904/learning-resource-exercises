%% Time-Frequency Analysis: scalogram matrix
% Source: https://matlabacademy.mathworks.com/v1/portal.html?course=otmltfa#chapter=4v1&lesson=2&section=2
% All four graded tasks received "Correct!" on 25 Sep 2026.
% INPUT: the course monitoredgearbox.mat is required and is not bundled.
% TOOLBOX: Wavelet Toolbox is required for cwt.
% Observed w: 110x40000 complex.
% The Task 1 semicolon suppresses a large display. Separate named figures
% retain both slices. These standalone display adaptations were not
% independently executed.

%% Course setup
load monitoredgearbox.mat;

%% Task 1: retain bump-wavelet coefficients and frequencies
% The Academy submission omitted this semicolon.
[w,f]=cwt(monitoredGear,"bump",fs);

%% Task 2: squared coefficient magnitudes
p=abs(w).^2;

%% Task 3: first time slice
firstslice=p(:,1);
figure('Name','First gearbox scalogram time slice');
plot(f,firstslice);

%% Task 4: last time slice
lastslice=p(:,end);
figure('Name','Last gearbox scalogram time slice');
plot(f,lastslice);

% The conceptual follow-up describes the 2 kHz fault component; it is
% supplied course feedback, not an additional run or measured result.
