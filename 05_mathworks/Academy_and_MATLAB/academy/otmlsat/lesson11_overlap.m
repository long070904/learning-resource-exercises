%% Spectral Analysis Techniques: verified Welch overlap exercise
% Source: https://matlabacademy.mathworks.com/details/spectral-analysis-techniques/otmlsat
% The graded slider task passed at overlap fraction 0.5.
% The ungraded 0.8-overlap follow-up completed with one output, and six
% vertical reference lines were visible in the course plot.
% INPUT: the course brokenouterrace.mat is required and is not bundled here.
% Separate named figures preserve both stages outside the Live Editor;
% this .m display arrangement was not separately executed in Academy.

%% Course setup and graded half-overlap setting
load brokenouterrace.mat;
winlen=n/5;
w=kaiser(round(winlen),19);
numoverlap=round(0.5*winlen);
figure('Name','Welch estimate with 50 percent overlap');
pwelch(sig,w,numoverlap,2^12,fs);
ylim([-80 10]);

%% Verified ungraded follow-up: greater overlap and reference markers
% Observed values: winlen=2400 and numoverlap=1920.
numoverlap=round(0.8*winlen);
figure('Name','Welch estimate with 80 percent overlap');
pwelch(sig,w,numoverlap,2^12,fs);
ylim([-80 10]);
loc=[2*fr frO 2*frO 3*frO 4*frO 5*frO];
xline(loc/1000,"m--");
% The marker conversion above preserves the exact course plotting code.
