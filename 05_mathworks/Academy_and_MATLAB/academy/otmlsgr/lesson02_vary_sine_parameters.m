%% Signal Generation and Resampling: sine-parameter activity
% Source: https://matlabacademy.mathworks.com/details/signal-generation-and-resampling/otmlsgr
% Lesson: Generate a Signal (2/2), Vary Sine Parameters.
% This is the final code revealed from the course varyparams.mlx Live Script
% using Output on Right, after changing its GUI controls in order:
% amplitude 1 -> 2, frequency 1 -> 3, phase 0 -> 1.57.
% Each plot was visually verified. The final Live Script section completed
% with one output. This was ungraded and is counted once as a GUI activity.
% Export adaptation: a named figure keeps this plot separate from earlier
% scripts. This .m figure arrangement was statically reviewed, not executed.

A=2;
f=3;
phi=1.57;
fs=8000;
dt=1/fs;
T=2;
t=(0:dt:T)';
sineWave=A*sin(2*pi*f*t+phi);
figure('Name','Vary Sine Parameters - final settings');
plot(t,sineWave);
ylim([-5 5]);
