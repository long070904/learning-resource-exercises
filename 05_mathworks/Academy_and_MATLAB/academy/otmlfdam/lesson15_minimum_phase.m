%% Reduce FIR Filter Delay
% Source: https://matlabacademy.mathworks.com/v1/portal.html?course=otmlfdam#chapter=6v1&lesson=2&section=2
% Academy source: whalemindelay.mlx
% Requires course whalesound.wav, absorption.m, and Signal Processing Toolbox.
% Course assets not bundled; standalone replay not independently run.
[whaley,fs] = audioread("whalesound.wav");
n = numel(whaley);
fr = (0:n-1)*(fs/n);
fr = fr(1:n/2+1);
waterabs = absorption(fr);
f = fr/fs*2;
b = fir2(10,f,waterabs);
[z,p] = tf2zpk(b,1);
figure; zplane(z,p)

%% Task 1 (Correct! observed 28 Sep 2026)
bmin = polystab(b);
bmin = bmin*norm(b)/norm(bmin);

%% Task 2 (Correct! observed 28 Sep 2026)
[z,p] = tf2zpk(bmin,1);
figure; zplane(z,p)
%% Task 3 (Correct! observed 28 Sep 2026)
figure; grpdelay(b,1,[],fs)
hold on
grpdelay(bmin,1,[],fs)
hold off
%% Further Practice: both returned logical 1 in Academy (28 Sep 2026)
islinphase(b)
isminphase(bmin)
