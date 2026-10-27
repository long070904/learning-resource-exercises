%% Spectral Analysis Techniques: resolve a small tone
% Source: https://matlabacademy.mathworks.com/details/spectral-analysis-techniques/otmlsat
% The graded slider task passed with beta=10. The course plot showed all
% three peak markers aligned with the reference-frequency lines.
% INPUT: the course psdsig.mat is required and is not bundled here.
% This saved script fixes the verified slider setting in the course code.

load psdsig;
n=length(t);
y1=sin(2*pi*fr*t);
y2=.01*sin(2*pi*3*fr*t);
y3=2*sin(2*pi*4*fr*t);
sig=1e-3*(y1+y2+y3);
beta=10;
[p,f]=periodogram(sig,kaiser(n,beta),2^12,fs);
figure;
findpeaks(10*log10(p),f,NPeaks=3,SortStr="descend");
xline(fr,"m--","f_r");
xline(3*fr,"m--","3f_r");
xline(4*fr,"m--","4f_r");

% See lesson07_tiny_tones_gui.md for the separate ungraded window comparison.
