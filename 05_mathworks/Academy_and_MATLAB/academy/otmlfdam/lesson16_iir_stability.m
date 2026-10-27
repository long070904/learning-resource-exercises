%% IIR Filter Stability
% Source: https://matlabacademy.mathworks.com/v1/portal.html?course=otmlfdam#chapter=6v1&lesson=3&section=1
% Academy source: iirabsfiltstability.mlx
% Requires course whalesound.wav, absorption.m, and Signal Processing Toolbox.
% Course assets not bundled; standalone replay not independently run.
[whaley,fs] = audioread("whalesound.wav");
n = numel(whaley);
fr = (0:n-1)*(fs/n);
fr = fr(1:n/2+1);
waterabs = absorption(fr);
fabs = fr/fs*2;

[b,a] = yulewalk(10,fabs,waterabs);

%% Task 1 (Correct! observed 28 Sep 2026)
[z,p] = tf2zpk(b,a);
figure; zplane(z,p)
%% Task 2 (Correct! observed 28 Sep 2026)
% Academy edited the earlier design. Replay recalculates the poles explicitly.
[b,a] = yulewalk(100,fabs,waterabs);
[z,p] = tf2zpk(b,a);
figure; zplane(z,p)
%% Further Practice (completed with two outputs, 28 Sep 2026)
% This high-order experiment produced rank-deficiency warnings in Academy.
% The time-domain output reached a 10^304 plot scale, illustrating failure.
whalefilt = filter(b,a,whaley);
t = (0:numel(whaley)-1)'/fs;
figure; plot(t,whaley)
hold on
plot(t,whalefilt)
hold off
xlabel("Time (sec)")
legend("original","filtered")
figure
impz(b,a,[],fs)
