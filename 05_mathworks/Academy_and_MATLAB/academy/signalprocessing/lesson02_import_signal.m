%% Signal Processing Onramp: verified import task
% Portal: https://matlabacademy.mathworks.com/v1/portal.html?course=signalprocessing#chapter=2v1&lesson=2&section=1
% The graded task received "Correct!" in the hosted Academy runtime.
% The ungraded follow-up also finished and created one output.
% INPUT: harp.csv exists in the course runtime. It has not been downloaded
% into this package; running this file elsewhere requires that actual asset.

%% Task 1: load samples as a numeric matrix
% Plotting this numeric vector uses sample positions on the horizontal axis.
harp = readmatrix("harp.csv");
plot(harp);

%% Ungraded follow-up: attach the known sampling rate
% A 50 Hz rate means each adjacent sample is separated by 1/50 = 0.02 s.
% The timetable carries that time base for the plot.
harpTT = readtimetable("harp.csv",SampleRate=50);
plot(harpTT,"Var1");
