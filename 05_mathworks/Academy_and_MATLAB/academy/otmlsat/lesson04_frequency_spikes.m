%% Spectral Analysis Techniques: verified frequency-peak tasks
% Source: https://matlabacademy.mathworks.com/details/spectral-analysis-techniques/otmlsat
% Lesson: Find Frequency Spikes. Both tasks received "Correct!" in Academy.
% INPUT: the course psdsig.mat is required and is not bundled here.

%% Course-provided startup
load psdsig;
sig=1e-3*sin(2*pi*fr*t);
n=length(sig);
[p,f]=periodogram(sig,ones(n,1),n*1,fs);
pwr=10*log10(p);
plot(f,pwr,"o");

%% Task 1: locate the largest spectral peak
[peak,loc]=findpeaks(pwr,f,NPeaks=1,SortStr="descend");

%% Task 2: calculate its frequency error
e=abs(fr-loc);

% The follow-up was conceptual only, without another executed example.
