%% Spectral Analysis Techniques: verified FFT tasks
% Source: https://matlabacademy.mathworks.com/details/spectral-analysis-techniques/otmlsat
% All five tasks received "Correct!" in the hosted Academy runtime.
% INPUT: psdsig.mat is supplied by the course and is not bundled here.
% Named figures are a saved-script adaptation to preserve both plots outside
% the Live Editor. This .m display arrangement was not separately executed.

%% Course-provided startup
load psdsig.mat;
whos;
% Observed workspace: fr, fs, n scalar; sig and t each 2400-by-1.

%% Task 1: calculate the discrete Fourier transform
Y=fft(sig);

%% Task 2: obtain the number of signal samples
n=length(sig);

%% Task 3: construct the transform's frequency grid
f=(0:n-1)*(fs/n);

%% Task 4: plot squared transform magnitude
p=abs(Y).^2;
figure('Name','Squared FFT magnitude');
plot(f,p);

%% Task 5: display the same values on a decibel scale
figure('Name','Squared FFT magnitude in decibels');
plot(f,10*log10(p));

% The conceptual follow-up inspected the existing peaks. No additional
% execution is counted. The course p here is squared FFT magnitude without
% a PSD normalization; the expressions above preserve the accepted code.
