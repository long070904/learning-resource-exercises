%% Spectral Analysis Techniques: parametric spectrum estimates
% Source: https://matlabacademy.mathworks.com/v1/portal.html?course=otmlsat#chapter=7v1&lesson=2&section=1
% The graded sample-count task received "Correct!" at n=50 on 25 Sep 2026.
% The n=20, n=30, and n=50 course plots were compared before the n=50
% submission. The further-practice comparison completed with five outputs.
% Separate named figures retain the five displays in a standalone .m file;
% that display adaptation was not separately executed in native MATLAB.

%% Course signal with the verified sample count
n=50;
fs=2000;
t=(0:n-1)'/fs;
x1=sin(2*pi*200*t);
x2=sin(2*pi*250*t);
rng default;
y=x1+x2+1e-2*randn(size(t));

%% Course Burg estimate
figure('Name','Burg autoregressive spectrum');
pburg(y,8,2^10,fs);

%% Verified ungraded comparison: three other parametric methods
figure('Name','Yule-Walker autoregressive spectrum');
pyulear(y,8,2^10,fs);
figure('Name','Covariance autoregressive spectrum');
pcov(y,8,2^10,fs);
figure('Name','Modified covariance autoregressive spectrum');
pmcov(y,8,2^10,fs);

%% Course periodogram comparison
figure('Name','Periodogram with 50 samples');
periodogram(y,[],2^10,fs);
