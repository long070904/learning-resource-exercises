%% Spectral Analysis Techniques: healthy-fan example
% Source: https://matlabacademy.mathworks.com/details/spectral-analysis-techniques/otmlsat
% Course example genfansig.mlx completed in Academy with one output.
% This is an ungraded example, not an FFT exercise pass.
% The rotation rate is 4000 rpm, which is 4000/60 Hz.

fs=2400;
n=2400;
t=(0:n-1)/fs;
t=t';
fr=4000/60;
sig=1e-3*(sin(2*pi*fr*t)+0.5*sin(2*pi*3*fr*t)+2*sin(2*pi*4*fr*t));
plot(t,sig);
