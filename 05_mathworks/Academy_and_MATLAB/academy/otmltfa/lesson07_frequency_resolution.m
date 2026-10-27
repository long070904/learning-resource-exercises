%% Time-Frequency Analysis: improve frequency resolution
% Source: https://matlabacademy.mathworks.com/v1/portal.html?course=otmltfa#chapter=4v1&lesson=2&section=1
% The graded task received "Correct!" on 25 Sep 2026.
% INPUT: the course monitoredgearbox.mat is required and is not bundled.
% TOOLBOX: Wavelet Toolbox is required for cwt.
% Separate figures preserve the default and bump-wavelet displays; this
% standalone display adaptation was not independently executed.

%% Course starting display
load monitoredgearbox.mat;
figure('Name','Gearbox scalogram with default wavelet');
cwt(monitoredGear,fs);

%% Task 1: bump wavelet
figure('Name','Gearbox scalogram with bump wavelet');
cwt(monitoredGear,"bump",fs);

% The follow-up only offered progression and added no activity.
