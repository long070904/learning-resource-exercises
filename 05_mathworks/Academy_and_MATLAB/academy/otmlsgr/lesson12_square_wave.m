%% Signal Generation and Resampling: verified square-wave project
% Source: https://matlabacademy.mathworks.com/details/signal-generation-and-resampling/otmlsgr
% Project: Generate and Resample a Square Wave.
% All five tasks received "Correct!" in the hosted Academy runtime.
% The ungraded sumOddHarmonics(10) call completed with one output.
% Keep the supplied sumOddHarmonics.m helper on the MATLAB path.
% Saved-script adaptation: named figures keep successive plots separate.
% This display arrangement was not separately executed as a .m file.

%% Task 1: construct the sampling grid
fs=100;
t=(0:1/fs:3)';

%% Task 2: generate the fundamental component
y1=sin(2*pi*t);

%% Task 3: add the third harmonic
y3=sin(2*pi*3*t)/3;
figure('Name','Fundamental plus third harmonic');
plot(t,y1+y3);

%% Task 4: calculate the target sample-rate ratio
fsup=200;
[p,q]=rat(fsup/fs);

%% Task 5: resample the approximation and inspect its spectrum
squareup=resample(y1+y3,p,q);
figure('Name','Resampled square-wave approximation spectrum');
pspectrum(squareup,fsup);

%% Ungraded follow-up: use ten odd harmonics
figure('Name','Ten-harmonic square-wave approximation');
sumOddHarmonics(10);
