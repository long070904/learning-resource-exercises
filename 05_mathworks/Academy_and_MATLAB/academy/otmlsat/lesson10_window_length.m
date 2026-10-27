%% Spectral Analysis Techniques: verified window-length settings
% Source: https://matlabacademy.mathworks.com/details/spectral-analysis-techniques/otmlsat
% All four slider tasks passed for numsegments = 2, 3, 15, and 20.
% INPUT: the course brokenouterrace.mat is required and is not bundled.
% The course displayed n=12000.
% ADAPTATION: the loop replays all verified settings in separate figures.
% This complete .m replay was not separately executed in Academy.

load brokenouterrace.mat;
testedSegments=[2 3 15 20];
for numsegments=testedSegments
    winlen=n/numsegments;
    w=kaiser(round(winlen),19);
    figure('Name',char("Welch estimate with "+numsegments+" segments"));
    pwelch(sig,w,0,2^12,fs);
    ylim([-80 10]);
end

% Follow-up/background explanations were read only, with no additional run.
