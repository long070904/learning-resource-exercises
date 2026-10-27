%% Signal Processing Onramp: verified signal-generation tasks
% Course: signalprocessing
% Portal: https://matlabacademy.mathworks.com/v1/portal.html?course=signalprocessing#chapter=1v1&lesson=2&section=1
% Tasks 1-5 each received "Correct!" in the hosted Academy runtime.
% The ungraded follow-up also finished and created one output.
% See ../../ACADEMY_PROGRESS.md for the current course-wide status.

%% Task 1: construct the sampling grid
% A 100 Hz sample rate gives a 0.01 second interval. The colon expression
% includes both endpoints, so this one-second grid contains 101 samples.
fs=100;
t=0:1/fs:1;

%% Task 2: generate and display the periodic component
% Multiplying cycles per second by time and 2*pi gives phase in radians.
sig=sin(2*pi*5*t);
plot(t,sig);

%% Task 3: create a noise vector with matching dimensions
% randn draws fresh normal samples; scaling controls their standard deviation.
% The saved submission intentionally has no random seed, as in the task.
noise=0.1*randn(size(sig));

%% Task 4: inspect the noisy sinusoid
% The two vectors share the same time grid and dimensions.
sigNoisy = sig + noise;
plot(t,sigNoisy);

%% Task 5: replace the sinusoid with a square wave
% The phase expression keeps the same five cycles per second.
sq = square(2*pi*5*t);
plot(t,sq);

%% Ungraded follow-up: add the same noise to the square wave
% The Academy runtime confirmed this section finished with one output.
% It is an ungraded section, so it does not count as another graded pass.
sqNoisy = sq + noise;
plot(t,sqNoisy);
