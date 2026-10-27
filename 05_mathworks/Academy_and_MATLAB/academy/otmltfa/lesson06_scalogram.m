%% Time-Frequency Analysis: scalogram
% Source: https://matlabacademy.mathworks.com/v1/portal.html?course=otmltfa#chapter=4v1&lesson=1&section=3
% Both graded tasks received "Correct!" in Academy on 25 Sep 2026.
% INPUT: the course monitoredgearbox.mat is required and is not bundled.
% TOOLBOX: Wavelet Toolbox is required for cwt.
% Separate named figures retain the full and limited-frequency scalograms;
% this standalone display adaptation was not independently executed.

%% Course setup
load monitoredgearbox.mat;

%% Task 1: full scalogram
figure('Name','Full gearbox scalogram');
cwt(monitoredGear,fs);

%% Task 2: limit frequencies to 1-2500 Hz
figure('Name','Gearbox scalogram from 1 to 2500 Hz');
cwt(monitoredGear,fs,FrequencyLimits=[1 2500]);

% The course follow-up only offered progression, with no extra activity.
