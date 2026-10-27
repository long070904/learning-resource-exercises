%% Signal Generation and Resampling: verified initial signal exercise
% Course: otmlsgr
% Source: https://matlabacademy.mathworks.com/details/signal-generation-and-resampling/otmlsgr
% Lesson: Generate Digital Signals > Generate a Signal (1/2).
% Tasks 1-3 each received "Correct!" in the hosted Academy runtime.
% The ungraded spectrum section also completed and created one output.
% Export adaptation: named figures preserve the separate Live Script plots.
% This .m figure arrangement has been statically reviewed, not executed.

%% Task 1: define a three-second sampling grid
% A 100 Hz rate creates 0.01-second spacing. Including both endpoints gives
% 301 sample times between zero and three seconds.
fs=100;
t=0:1/fs:3;

%% Task 2: create and display a five-hertz component
sig=sin(2*pi*5*t);
figure('Name','Task 2 - five-hertz component');
plot(t,sig);

%% Task 3: add a three-hertz component
% The two sinusoidal components share the same sampling grid.
sig=sig+sin(2*pi*3*t);
figure('Name','Task 3 - combined components');
plot(t,sig);

%% Ungraded follow-up: inspect the power spectrum
% Verified runtime result: section completed with one output.
figure('Name','Ungraded follow-up - combined power spectrum');
pspectrum(sig,fs);
