%% Signal Processing Onramp: verified alignment tasks
% Portal: https://matlabacademy.mathworks.com/v1/portal.html?course=signalprocessing#chapter=3v1&lesson=5&section=1
% Both graded alignment submissions received "Correct!" in Academy.
% INPUT: processedsignals.mat is supplied in the hosted course runtime.
% It has not been downloaded into this package. Running this file elsewhere
% requires that actual course asset and MATLAB's Signal Processing Toolbox.

%% Course input
% The lesson provides this MAT-file load before the graded operations.
load("processedsignals.mat");
% Observed pair delays: harp/pax -596, harp/wanc 1167, pax/wanc 1770.
% The exercise used wanc as the latest arrival and aligned the others to it.

%% Task 1: align the first pair
[harp,wanc] = alignsignals(harp,wanc);

%% Task 2: align the remaining recording
[pax,wanc] = alignsignals(pax,wanc);
% The course's existing plot displayed all three aligned signals after this.
% Its plotting cell is not reproduced here because its exact code was not
% recorded with the verified submissions.

%% Ungraded follow-up: inspect the recordings before alignment
% Reload into a structure to preserve the already aligned workspace arrays.
% This exact follow-up ran successfully and produced one output in Academy.
original = load("processedsignals.mat");
plot([original.harp,original.pax,original.wanc]);
title("Before alignment");
