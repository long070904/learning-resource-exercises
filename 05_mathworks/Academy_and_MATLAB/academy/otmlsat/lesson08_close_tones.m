%% Spectral Analysis Techniques: resolve closely spaced tones
% Source: https://matlabacademy.mathworks.com/details/spectral-analysis-techniques/otmlsat
% The single graded slider task received "Correct!" with beta=0.
% The course plot showed both peak markers aligned with the reference lines.
% This saved script fixes that verified slider setting in the course code.

fs=75;
t=(0:1/fs:1.6)';
y1=sin(2*pi*25*t);
y2=sin(2*pi*26*t);
y=y1+y2;
n=length(y1);
beta=0;
[p,f]=periodogram(y,kaiser(n,beta),2^12,fs);
figure;
findpeaks(10*log10(p),f,NPeaks=2,SortStr="descend");
xline(25,"m--");
xline(26,"m--");

% Further practice was conceptual only and adds no execution count.
