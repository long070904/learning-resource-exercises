%% Spectral Analysis Techniques: verified precision setting
% Source: https://matlabacademy.mathworks.com/details/spectral-analysis-techniques/otmlsat
% The slider's exponent was set to 18 and its one graded check returned
% "Correct!". The triggered course run completed with six outputs.
% INPUT: the course psdsig.mat is required and is not bundled here.
% This saved code fixes the verified slider value in the course calculation.
% It is one graded task, not an additional ungraded run.

load psdsig.mat;
sig=1e-3*sin(2*pi*fr*t);
n=length(sig);
nfft=2^18;
[p,f]=periodogram(sig,ones(n,1),nfft,fs);
pwr=10*log10(p);
figure;
plot(f,pwr,".");
[peak,loc]=findpeaks(pwr,f,NPeaks=1,SortStr="descend");
e=abs(fr-loc);

% Observed rounded display: nfft 262144, loc 66.6687 Hz, e 0.0020 Hz.
% The conceptual follow-up recommended 2^12 points for remaining course work.
% No separate execution of that recommendation is counted here.
