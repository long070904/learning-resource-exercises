%% FIR Zero-Pole Plot
% Source: https://matlabacademy.mathworks.com/v1/portal.html?course=otmlfdam#chapter=6v1&lesson=2&section=1
% Academy source: movavgzp.mlx
% Requires course whalesound.wav, absorption.m, and Signal Processing Toolbox.
% External course assets not bundled; standalone replay not independently run.
[whaley,fs] = audioread("whalesound.wav");
n = numel(whaley);
fr = (0:n-1)*(fs/n);
fr = fr(1:n/2+1);
waterabs = absorption(fr);
fabs = fr/fs*2;

a = 1;
b = fir2(30,fabs,waterabs);

%% Task 1 (Correct! observed 28 Sep 2026)
[z,p,k] = tf2zpk(b,a);
%% Task 2 (Correct! observed 28 Sep 2026)
zplane(z,p)
% Follow-up: FIR poles at the origin imply stability.
