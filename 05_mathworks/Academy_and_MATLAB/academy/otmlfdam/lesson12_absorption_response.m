%% Create Desired Absorption Filter
% Source: https://matlabacademy.mathworks.com/v1/portal.html?course=otmlfdam#chapter=5v1&lesson=2&section=1
% Academy source: whaleabsfilt.mlx.
% Requires course whalesound.wav and simplified absorption.m helper.
% These course assets are not bundled. Standalone replay not independently run.
[whaley,fs] = audioread("whalesound.wav");
n = numel(whaley);
fr = (0:n-1)*(fs/n);
fr = fr(1:n/2+1);

%% Task 1 (Correct! observed 28 Sep 2026)
waterabs = absorption(fr);
%% Task 2 (Correct! observed 28 Sep 2026)
plot(fr,waterabs)
%% Further Practice (section completed with one output, 28 Sep 2026)
xlabel("Frequency (Hz)")
ylabel("Absorption (mag / km)")
